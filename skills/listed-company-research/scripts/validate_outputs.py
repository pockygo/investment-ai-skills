#!/usr/bin/env python3
"""Check fixed-schema Markdown financial tables; does not verify PDF semantics.

Amounts must already share the currency and million-unit basis. JSON lists every
error/warning. Exit 1 means errors; exit 0 only means these checks found no errors.
"""
import argparse
import json
import math
import re
from pathlib import Path

ANNUAL = '年份|营业收入|收入YoY|归母净利|净利YoY|扣非归母|综合毛利率|净利率|ROE(加权)|经营现金流净额|净现比|CAPEX|CAPEX/收入|存货|应收账款|有息负债|现金分红|研发投入占比'.split('|')
QUICK = '年份|营业收入|收入YoY|归母净利|净利YoY|扣非归母|毛利率|净利率|ROE|经营现金流净额|净现比|CAPEX|现金分红'.split('|')


def number(value):
    value = value.strip().replace(',', '').replace('，', '')
    if not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)%?', value):
        return None
    v = float(value.rstrip('%'))
    return v / 100 if value.endswith('%') else v


def tables(path):
    result, group = [], []
    for line in path.read_text(encoding='utf-8').splitlines() + ['']:
        if line.strip().startswith('|'):
            cells = [s.strip() for s in line.strip().strip('|').split('|')]
            if all(re.fullmatch(r':?-+:?', s) for s in cells):
                continue
            group.append(cells)
        elif group:
            result.append(group)
            group = []
    return result


def previous(key, n=1):
    serial = key[0] * 4 + key[1] - 1 - n
    return serial // 4, serial % 4 + 1


class Audit:
    def __init__(self):
        self.issues = []
        self.checked = 0

    def issue(self, message, level='error'):
        self.issues.append({'level': level, 'message': message})

    def compare(self, label, actual, expected, tolerance=0.25):
        if actual is None or expected is None:
            return
        self.checked += 1
        if not math.isclose(actual, expected, abs_tol=tolerance, rel_tol=1e-8):
            self.issue(f'{label}: reported={actual:g}, calculated/reference={expected:g}')

    def rows(self, path, select):
        found = []
        for tab in tables(path):
            if select(tab[0]):
                for row in tab[1:]:
                    if len(row) != len(tab[0]):
                        self.issue(f'{path.name}: row width {len(row)} != {len(tab[0])}')
                    else:
                        found.append((tab[0], row))
        return found


def run(project, report=None, profile=None):
    audit = Audit()
    annual_path = project / 'timeseries/财务时间序列.md'
    if not annual_path.exists():
        audit.issue('Missing annual series')
        return audit
    annual, headers = {}, {}
    rows = audit.rows(annual_path, lambda h: len(h) == 18 and h[0] == '年份')
    if not rows:
        audit.issue('No fixed-schema annual table found')
    for head, row in rows:
        if head != ANNUAL:
            audit.issue('Annual header differs from fixed 18-column schema')
        if row[0] in annual:
            audit.issue(f'Duplicate annual/interim period: {row[0]}')
        annual[row[0]], headers[row[0]] = row, head
    for period, row in annual.items():
        v = [number(s) for s in row]
        rev, net, ocf, capex = v[1], v[3], v[9], v[11]
        if rev:
            audit.compare(f'{period} net margin', v[7], net / rev if net is not None else None, .0006)
            audit.compare(f'{period} CAPEX/revenue', v[12], capex / rev if capex is not None else None, .0006)
        if net:
            audit.compare(f'{period} OCF/parent profit', v[10], ocf / net if ocf is not None else None, .006)
        if re.fullmatch(r'\d{4}', period) and str(int(period)-1) in annual:
            prev = annual[str(int(period)-1)]
            for col, yoy in [(1, 2), (3, 4)]:
                a, b = number(row[col]), number(prev[col])
                if b and a is not None:
                    audit.compare(f'{period} {ANNUAL[yoy]}', v[yoy], a / b - 1, .0006)
    if profile:
        seen = set()
        for head, row in audit.rows(profile, lambda h: len(h) == 18 and h[0] == '年份'):
            seen.add(row[0])
            if head != ANNUAL:
                audit.issue('Profile header differs from annual schema')
            if row[0] not in annual or row != annual[row[0]]:
                audit.issue(f'Profile {row[0]} is not an exact copy of annual/interim series')
        if seen != set(annual):
            audit.issue('Profile periods do not match annual/interim series')
    if report:
        seen = set()
        for head, row in audit.rows(report, lambda h: len(h) == 13 and h[0] == '年份'):
            seen.add(row[0])
            if head != QUICK:
                audit.issue('Quick table header differs from fixed 13-column schema')
            source = annual.get(row[0])
            if source is None:
                audit.issue(f'Quick table {row[0]} absent from master series')
                continue
            for i, idx in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16]):
                a, b = number(row[i]), number(source[idx])
                if a is not None and b is not None:
                    audit.compare(f'Quick {row[0]} {QUICK[i]}', a, b, 1e-8)
                elif row[i] != source[idx]:
                    audit.issue(f'Quick {row[0]} {QUICK[i]} differs from master series')
        if seen != set(annual):
            audit.issue('Quick table periods do not match master series')
    panel_path = project / 'timeseries/季度财务面板.md'
    if not panel_path.exists():
        audit.issue('No quarterly panel: verify whether fewer than four quarters supplied', 'warning')
        return audit
    def quarterly_rows(select):
        out = {}
        for _, row in audit.rows(panel_path, select):
            m = re.fullmatch(r'(\d{4})Q([1-4])', row[0])
            if m:
                key = int(m[1]), int(m[2])
                if key in out:
                    audit.issue(f'Duplicate quarter {row[0]}')
                out[key] = [number(s) for s in row]
        return out
    qa = quarterly_rows(lambda h: len(h) == 8 and h[:2] == ['季度', '营业收入'])
    qb = quarterly_rows(lambda h: len(h) == 8 and h[:2] == ['季度', '毛利率'])
    qc = quarterly_rows(lambda h: len(h) == 7 and h[:2] == ['季度', 'TTM 收入'])
    qe = quarterly_rows(lambda h: len(h) == 7 and h[:2] == ['季度', '应收账款'])
    if not qa:
        audit.issue('No standard quarterly scale table found')
    for key, a in sorted(qa.items()):
        label = f'{key[0]}Q{key[1]}'
        for delta, cols in [(1, [(1, 3), (4, 6)]), (4, [(1, 2), (4, 5)])]:
            prev = qa.get(previous(key, delta))
            if prev:
                for source, ratio in cols:
                    if prev[source] and a[source] is not None:
                        audit.compare(f'{label} growth col{ratio}', a[ratio], a[source] / prev[source] - 1, .0006)
        b = qb.get(key)
        if b and a[1] and a[4] is not None:
            audit.compare(f'{label} net margin across A/B', b[2], a[4] / a[1], .0006)
            if a[4] and b[4] is not None:
                audit.compare(f'{label} OCF/parent across A/B', b[5], b[4] / a[4], .006)
        c = qc.get(key)
        window = [qa.get(previous(key, i)) for i in range(4)]
        if c:
            for source, target in [(1, 1), (4, 3)]:
                complete = all(w is not None and w[source] is not None for w in window)
                if complete:
                    audit.compare(f'{label} TTM col{target}', c[target], sum(w[source] for w in window))
                elif c[target] is not None:
                    audit.issue(f'{label} TTM calculated without four consecutive complete quarters')
            prev = qc.get(previous(key, 4))
            if prev:
                for source, ratio in [(1, 2), (3, 4)]:
                    if prev[source] and c[source] is not None:
                        audit.compare(f'{label} TTM growth col{ratio}', c[ratio], c[source] / prev[source] - 1, .0006)
        if key[1] == 4 and str(key[0]) in annual:
            ar = [number(s) for s in annual[str(key[0])]]
            if c:
                audit.compare(f'{label} TTM revenue vs annual', c[1], ar[1])
                audit.compare(f'{label} TTM parent vs annual', c[3], ar[3])
            for qcol, acol in [(1, 1), (4, 3)]:
                if all(w is not None and w[qcol] is not None for w in window):
                    audit.compare(f'{label} quarter sum vs annual col{acol}', sum(w[qcol] for w in window), ar[acol])
            if key in qe:
                for qcol, acol in [(1, 14), (2, 13), (6, 15)]:
                    audit.compare(f'{label} closing balance vs annual col{acol}', qe[key][qcol], ar[acol])
    for table in [qb, qc, qe]:
        if set(table) != set(qa):
            audit.issue('Quarterly tables A/B/C/E have different period coverage')
    audit.issue('Not covered: source semantics, currency conversion in prose, restatement comparability, missing input periods, independent disclosure verification, valuation and claims. Review data-quality.md.', 'warning')
    return audit


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', type=Path, required=True)
    p.add_argument('--report', type=Path)
    p.add_argument('--profile', type=Path)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    def resolve(path):
        return path if path is None or path.is_absolute() else args.project / path
    audit = run(args.project, resolve(args.report), resolve(args.profile))
    errors = sum(i['level'] == 'error' for i in audit.issues)
    result = {'scope': 'Arithmetic and cross-table checks only; not source verification',
              'checked': audit.checked, 'errors': errors, 'issues': audit.issues}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output + '\n', encoding='utf-8')
    print(output)
    raise SystemExit(1 if errors else 0)


if __name__ == '__main__':
    main()
