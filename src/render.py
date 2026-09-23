# -*- coding: utf-8 -*-
"""產生 index.html（不要直接編 index.html，改 src/content.py 後跑 bash build.sh）

用法：python3 src/render.py
"""
import os
import sys
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import content as C # noqa: E402


def esc(t):
    return (t or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def esc_nl(t):
    """保留換行的文字（判讀準則、實例）"""
    return esc(t).replace('\n', '<br>')


def field(key, items, ind=' ', cls='field'):
    label, ph, hint = items[key]
    out = ['%s<div class="%s" data-item="%s">' % (ind, cls, esc(label))]
    out.append('%s <label class="field-label" for="%s">%s%s</label>'
               % (ind, key, esc(label),
                  '' if not hint else '<span class="field-tag">%s</span>' % esc(hint)))
    out.append('%s <textarea id="%s" class="worksheet-input" placeholder="%s"></textarea>'
               % (ind, key, esc(ph)))
    out.append('%s</div>' % ind)
    return out


def radio_row(key, opts, note_key, items, ind=' ', question=None):
    """是/否選項（+ 選填說明欄）。選項也會存檔（data-save）。"""
    ph = ''
    if note_key:
        ph = items[note_key][1]
        if question is None:
            question = items[note_key][0].split('：')[0]
    q = question or key
    out = ['%s<div class="radio-row" data-radio="%s">' % (ind, key),
           '%s <div class="radio-main">' % ind,
           '%s <span class="radio-q">%s</span>' % (ind, esc(q))]
    for val, text in opts:
        out.append('%s <label class="radio-opt"><input type="radio" name="%s" value="%s" '
                   'data-save="%s">%s</label>' % (ind, key, val, key, esc(text)))
    out.append('%s </div>' % ind)
    if note_key:
        out.append('%s <textarea id="%s" class="worksheet-input radio-note" placeholder="%s"></textarea>'
                   % (ind, note_key, esc(ph)))
    out.append('%s</div>' % ind)
    return out


def render_bcg_block(ind=' '):
    """BCG 多事業單位：每單位一列 + 自動繪製 2×2 + 摘要"""
    out = ['%s<div class="bcg-wrap">' % ind,
           '%s <div class="bcg-plot" id="bcgPlot">' % ind,
           '%s <div class="bcg-ylab">市場成長率 高 ↑</div>' % ind,
           '%s <div class="bcg-xlab">相對市佔（你 ÷ 最大對手） 高 →</div>' % ind,
           '%s <div class="bcg-grid">' % ind]
    # 2×2 用列優先排列；x 軸是「相對市佔 高 →」，所以左上必須是高成長×低市佔＝問號、
    # 右上才是明星。class 由象限 key 推導，不要再拿一份平行清單去 zip（會跟標籤對不上）。
    _grid_order = ['question', 'star', 'dog', 'cow']
    _by_key = {k: (n, note) for k, n, note in C.BCG_QUADRANTS}
    for key in _grid_order:
        name, note = _by_key[key]
        out.append('%s <div class="bcg-cell q-%s" data-q="%s"><span class="bcg-cellname">%s</span>'
                   '<span class="bcg-cellnote">%s</span></div>' % (ind, key, key, name, note))
    out += ['%s </div>' % ind,
            '%s </div>' % ind,
            '%s <div class="bcg-summary" id="bcgSummary"></div>' % ind,
            '%s</div>' % ind,
            '%s<div class="bcg-units" id="bcgUnits">' % ind]
    for n in range(1, C.BCG_MAX_UNITS + 1): # 全部產生，超過預設數量者先隱藏
        out += render_bcg_row(n, ind + ' ')
    out += ['%s</div>' % ind,
            '%s<div class="bcg-actions no-print">' % ind,
            '%s <button type="button" id="bcgAdd">＋ 新增事業單位</button>' % ind,
            '%s <span class="field-tag">最多 %d 個。移除的單位，內容會一起刪掉。</span>' % (ind, C.BCG_MAX_UNITS),
            '%s</div>' % ind]
    return out


def render_bcg_row(n, ind):
    """第 n 個事業單位"""
    q = 'bcg-%d-quadrant' % n
    out = ['%s<div class="bcg-row" data-unit="%d"%s>' % (ind, n, ' hidden' if n >C.BCG_DEFAULT_UNITS else ''),
           '%s <div class="bcg-row-head">事業單位 %d<button type="button" class="bcg-del no-print" data-del="%d">移除</button></div>'
           % (ind, n, n),
           '%s <div class="bcg-row-body">' % ind]
    k, label, ph = C.BCG_UNIT_FIELDS[0]
    out += ['%s <div class="field" data-item="%s">' % (ind, esc(label)),
            '%s <label class="field-label" for="bcg-%d-%s">%s</label>' % (ind, n, k, esc(label)),
            '%s <textarea id="bcg-%d-%s" class="worksheet-input bcg-name" placeholder="%s"></textarea>'
            % (ind, n, k, esc(ph)),
            '%s </div>' % ind]
    for fk, opts in [('growth', C.BCG_GROWTH_OPTIONS), ('share', C.BCG_SHARE_OPTIONS)]:
        key = 'bcg-%d-%s' % (n, fk)
        qq = '市場成長率' if fk == 'growth' else '相對市佔'
        out += ['%s <div class="radio-row" data-radio="%s" data-bcg="%s">' % (ind, key, fk),
                '%s <div class="radio-main"><span class="radio-q">%s</span>' % (ind, qq)]
        for val, text in opts:
            out.append('%s <label class="radio-opt"><input type="radio" name="%s" value="%s" '
                       'data-save="%s">%s</label>' % (ind, key, val, key, esc(text)))
        out += ['%s </div>' % ind, '%s </div>' % ind]
    out.append('%s <div class="verdict bcg-badge" id="%s"><span class="verdict-label">象限</span>'
               '<span class="verdict-text">選完成長率與相對市佔即自動判定。</span></div>' % (ind, q))
    k, label, ph = C.BCG_UNIT_FIELDS[1]
    out += ['%s <div class="field" data-item="%s">' % (ind, esc(label)),
            '%s <label class="field-label" for="bcg-%d-%s">%s</label>' % (ind, n, k, esc(label)),
            '%s <textarea id="bcg-%d-%s" class="worksheet-input" placeholder="%s"></textarea>'
            % (ind, n, k, esc(ph)),
            '%s </div>' % ind,
            '%s </div>' % ind,
            '%s</div>' % ind]
    return out


def render_section(sec):
    out = [' <section class="sheet-section" id="sec-%s">' % sec['key'],
           ' <h3 class="sheet-h3">%s %s</h3>' % (sec['num'], esc(sec['title'])),
           ' <p class="sheet-desc">%s</p>' % esc(sec['desc'])]
    if sec.get('criteria') or sec.get('example'):
        out.append(' <details class="fw-guide">')
        out.append(' <summary>判讀準則與實例</summary>')
        if sec.get('criteria'):
            out.append(' <div class="fw-criteria"><strong>判讀準則</strong><p>%s</p></div>'
                       % esc_nl(sec['criteria']))
        if sec.get('example'):
            out.append(' <div class="fw-example"><strong>實例</strong><p>%s</p></div>'
                       % esc_nl(sec['example']))
        out.append(' </details>')

    items = sec['items']
    for g in sec['layout']:
        kind = g[0]
        if kind == 'grid':
            out.append(' <div class="field-grid cols-%d">' % g[1])
            for k in g[2]:
                out += field(k, items, ' ')
            out.append(' </div>')
        elif kind == 'matrix':
            out.append(' <div class="matrix-2x2">')
            for k in g[2]:
                out += field(k, items, ' ', 'field mx-cell')
            out.append(' </div>')
        elif kind == 'list':
            for k in g[1]:
                out += field(k, items)
        elif kind == 'radio':
            out += radio_row(g[1], g[2], g[3], items, question=(g[4] if len(g) >4 else None))
        elif kind == 'bcgmatrix':
            out += render_bcg_block()
        elif kind == 'verdict':
            out.append(' <div class="verdict" id="%s-verdict">' % g[1])
            out.append(' <span class="verdict-label">自動判定</span>')
            out.append(' <span class="verdict-text">把上面的選項選完，這裡會自動算出結論。</span>')
            out.append(' </div>')
    out.append(' </section>')
    return out


def render_analysis_sections():
    out = []
    for sec in C.ANALYSIS:
        out += render_section(sec)
        out.append(' ')
    return out


def read_field(key, items, ind=' '):
    label, ph, _ = items[key]
    return ['%s<div class="field" data-item="%s">' % (ind, esc(label)),
            '%s <label class="field-label" for="%s">%s</label>' % (ind, key, esc(label)),
            '%s <textarea id="%s" class="worksheet-input" placeholder="%s"></textarea>'
            % (ind, key, esc(ph)),
            '%s</div>' % ind]


def render_stage_pane(stage):
    m = C.STAGE_META[stage]
    out = [' <div id="tab-content-%s" class="tab-content" role="tabpanel" aria-labelledby="tab-btn-%s">'
           % (stage, stage),
           ' <section class="stage-section">',
           ' <h2 class="stage-title">%s</h2>' % esc(m['pane_title']),
           ' <div class="stage-focus">',
           ' <h3>本階段重點</h3>',
           ' <ul>',
           ' <li><strong>核心目標：</strong>%s</li>' % esc(m['goal']),
           ' <li><strong>主要挑戰：</strong>%s</li>' % esc(m['challenge']),
           ' </ul>',
           ' <p class="stage-reading">%s</p>' % esc(m['reading']),
           ' <p class="stage-refs">回頭看：%s</p>' % esc('、'.join(C.STAGE_READING_TOOLS[stage])),
           ' </div>',
           ' <div class="tool-block">',
           ' <label class="tool-label">階段判讀</label>',
           ' <p class="tool-description">分析在「現況與分析」分頁做一次就好；'
           '這裡只回答這個階段特有的問題。</p>']
    for k in m['items']:
        out += read_field(k, m['items'])
    out += [' </div>',
            ' </section>',
            ' </div>']
    return out


def render_action_pane():
    a = C.ACTION_INTRO
    ph = {'what': '例如：推出月租 40 席方案', 'owner': '誰負責、有沒有決定權',
          'due': 'YYYY-MM-DD', 'metric': '可被外人驗證的數字'}
    out = [' <div id="tab-content-actions" class="tab-content" role="tabpanel" aria-labelledby="tab-btn-actions">',
           ' <section class="stage-section">',
           ' <h2 class="stage-title">%s</h2>' % esc(a['title']),
           ' <p class="sheet-desc">%s</p>' % esc(a['desc']),
           ' <div class="fw-example"><strong>實例</strong><p>%s</p></div>' % esc_nl(a['example'])]
    for r in range(1, C.ACTION_ROWS + 1):
        out.append(' <div class="action-row" data-row="%d">' % r)
        out.append(' <div class="action-head">第 %d 項</div>' % r)
        out.append(' <div class="field-grid cols-2">')
        for fk, fl in C.ACTION_FIELDS:
            key = 'act-%d-%s' % (r, fk)
            out.append(' <div class="field" data-item="%s">' % esc(fl))
            out.append(' <label class="field-label" for="%s">%s</label>' % (key, esc(fl)))
            out.append(' <textarea id="%s" class="worksheet-input" placeholder="%s"></textarea>'
                       % (key, esc(ph[fk])))
            out.append(' </div>')
        # 狀態（下拉，會存檔）
        key = 'act-%d-status' % r
        out.append(' <div class="field">')
        out.append(' <label class="field-label" for="%s">狀態</label>' % key)
        out.append(' <select id="%s" class="status-select" data-save="%s">' % (key, key))
        for val, txt in C.ACTION_STATUS:
            out.append(' <option value="%s">%s</option>' % (val, esc(txt)))
        out.append(' </select>')
        out.append(' </div>')
        out.append(' </div>')
        out.append(' </div>')
    out += [' <div class="action-summary" id="actionSummary"></div>',
            ' <div class="bcg-actions no-print">',
            ' <button type="button" id="actionReviewBtn">記錄本次檢視（把「今天看過」記下來）</button>',
            ' <span class="field-tag">期限格式用 YYYY-MM-DD，逾期且未完成的項目會自動標紅。</span>',
            ' </div>',
            ' </section>',
            ' </div>']
    return out


def main():
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()

    html = tpl.replace('<!--{{ANALYSIS_SECTIONS}}-->', '\n'.join(render_analysis_sections()))
    # 舊存檔對應表由 content.py 產生（單一真實來源），注入到頁面的 JS
    def jsval(v):
        if isinstance(v, (list, tuple)):
            return '[' + ', '.join(jsval(x) for x in v) + ']'
        return '"%s"' % str(v).replace('"', '\\"')
    mig = [' "%s": %s' % (k, jsval(vs)) for k, vs in C.ID_MIGRATION.items()]
    html = html.replace('{{TITLE}}', C.TITLE)
    html = html.replace('{{SCHEMA_VERSION}}', str(C.SCHEMA_VERSION))
    html = html.replace('{{ACTION_ROWS}}', str(C.ACTION_ROWS))
    html = html.replace('{{BCG_MAX_UNITS}}', str(C.BCG_MAX_UNITS))
    html = html.replace('{{BCG_DEFAULT_UNITS}}', str(C.BCG_DEFAULT_UNITS))
    html = html.replace('{{ID_MIGRATION_V2}}', '{\n' + ',\n'.join(
        ' "%s": %s' % (k, jsval(vs)) for k, vs in C.ID_MIGRATION_V2.items()) + '\n }')
    html = html.replace('{{ID_MIGRATION}}', '{\n' + ',\n'.join(mig) + '\n }')

    panes = []
    for i, s in enumerate(C.STAGES):
        if i:
            panes.append(' ')
        panes += render_stage_pane(s)
    panes.append(' ')
    panes += render_action_pane()
    html = html.replace('<!--{{STAGE_PANES}}-->', '\n'.join(panes))

    left = re.findall(r'<!--\{\{[A-Z_]+\}\}-->', html)
    if left:
        raise SystemExit('未替換的標記：%s' % left)

    # 防呆：JS 若引用 Python 常數，頁面上必須有對應 const 宣告
    # （少了宣告不會是語法錯誤，只會在執行時拋 ReferenceError 然後被 try/catch 吞掉）
    for name in ('SCHEMA_VERSION', 'ACTION_ROWS', 'BCG_MAX_UNITS', 'BCG_DEFAULT_UNITS'):
        if re.search(r'\b%s\b' % name, html) and ('const %s = ' % name) not in html:
            raise SystemExit('產生失敗：JS 用到 %s 但頁面沒有 const 宣告（未注入？）' % name)

    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)

    ids = re.findall(r'<textarea[^>]*id="([^"]+)"', html)
    dup = sorted({x for x in ids if ids.count(x) >1})
    n_an = sum(len(s['items']) for s in C.ANALYSIS)
    n_rd = sum(len(m['items']) for m in C.STAGE_META.values())
    n_ac = C.ACTION_ROWS * len(C.ACTION_FIELDS)
    n_bcg = C.BCG_MAX_UNITS * len(C.BCG_UNIT_FIELDS)
    print('產生 index.html：%d bytes' % len(html.encode()))
    print(' 文字欄位 %d 個（分析 %d + BCG 事業單位 %d + 判讀 %d + 行動 %d）%s'
          % (len(ids), n_an, n_bcg, n_rd, n_ac, '' if not dup else '，重複 id: %s' % dup))
    assert len(ids) == n_an + n_bcg + n_rd + n_ac, '欄位數對不上：%d vs %d' % (len(ids), n_an + n_bcg + n_rd + n_ac)
    print(' BCG 事業單位列 %d 列（預設顯示 %d）、行動狀態下拉 %d 個'
          % (len(re.findall(r'class="bcg-row"', html)), C.BCG_DEFAULT_UNITS, len(re.findall(r'<select[^>]*data-save="', html))))
    n_radio = len(re.findall(r'<input type="radio"[^>]*data-save="', html))
    n_sel = len(re.findall(r'<select[^>]*data-save="', html))
    print(' 是/否選項 %d 個、下拉 %d 個、分析區塊 %d 個、階段 %d 個、判讀準則 %d 段'
          % (n_radio, n_sel, len(C.ANALYSIS), len(C.STAGES),
             sum(1 for s in C.ANALYSIS if s.get('criteria'))))


if __name__ == '__main__':
    main()
