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

import content as C   # noqa: E402


def esc(t):
    return (t or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def field_id(key, stage):
    """欄位 id 一律由 key + 階段組成；例外見 content.ID_OVERRIDES。"""
    return C.ID_OVERRIDES.get(key) or '%s-%s' % (key, stage)


def render_group(key, stage, items, cls, ind):
    label, ph, hint = items[key]
    out = ['%s<div class="%s">' % (ind, cls)]
    if label:
        out.append('%s    <label for="%s" class="sub-label">%s</label>'
                   % (ind, field_id(key, stage), esc(label)))
    if hint:
        out.append('%s    <span class="sub-label-hint">%s</span>' % (ind, esc(hint)))
    out.append('%s    <textarea id="%s" class="worksheet-input" placeholder="%s"></textarea>'
               % (ind, field_id(key, stage), esc(ph)))
    out.append('%s</div>' % ind)
    return out


def render_tool_block(fw_key, stage):
    d = C.FRAMEWORKS[fw_key]['stages'][stage]
    out = ['                <div class="tool-block">',
           '                    <label class="tool-label">%s</label>' % esc(d['title']),
           '                    <p class="tool-description">%s</p>' % esc(d['desc'])]
    grids = 0
    for kind, keys in d['layout']:
        if kind == 'grid':
            out.append('                    <div class="toolkit">')
            for k in keys:
                out += render_group(k, stage, d['items'], 'input-group', '                        ')
            out.append('                    </div>')
            grids += 1
        elif kind == 'single':
            # 版面慣例：排在矩陣前面用 mb-4（下方留白），排在矩陣後面用 mt-4（上方留白）
            cls = 'input-group mb-4' if grids == 0 else 'input-group mt-4'
            for k in keys:
                out += render_group(k, stage, d['items'], cls, '                    ')
        elif kind == 'bare':
            for k in keys:
                out.append('                    <textarea id="%s" class="worksheet-input" placeholder="%s"></textarea>'
                           % (field_id(k, stage), esc(d['items'][k][1])))
    out.append('                </div>')
    return out


def render_carry_bar(stage):
    m = C.STAGE_META[stage]
    if not m.get('carry_from'):
        return []
    return ['                <div class="carry-bar no-print">',
            '                    <button type="button" class="carry-btn" data-carry="%s">⤵ 帶入%s的%s</button>'
            % (stage, m['carry_label_from'], m['carry_tools']),
            '                    <span class="carry-hint">只複製上一階段「已填寫」的同框架欄位。目標欄位若已有內容會接在後面，不覆蓋。</span>',
            '                </div>']


def render_stage_pane(stage):
    m = C.STAGE_META[stage]
    out = ['        <div id="tab-content-%s" class="tab-content" role="tabpanel" aria-labelledby="tab-btn-%s">' % (stage, stage),
           '            <section class="stage-section">',
           '                <h2 class="stage-title">%s</h2>' % esc(m['pane_title'])]
    out += render_carry_bar(stage)
    out += ['                <div class="stage-focus">',
            '                    <h3>本階段重點</h3>',
            '                    <ul>',
            '                        <li><strong>核心目標：</strong>%s</li>' % esc(m['goal']),
            '                        <li><strong>主要挑戰：</strong>%s</li>' % esc(m['challenge']),
            '                    </ul>',
            '                </div>']
    for fw_key in C.STAGE_ORDER[stage]:
        out += render_tool_block(fw_key, stage)
    out += ['            </section>',
            '        </div>']
    return out


def render_overview_sections():
    out = []
    for i, stage in enumerate(C.STAGES):
        ov = C.OVERVIEW[stage]
        m = C.STAGE_META[stage]
        out.append('            <section class="analysis-section">')
        out.append('                <h2 class="analysis-h2">%s</h2>' % esc(ov['heading']))
        out.append('                <h3 class="analysis-h3">階段重點：</h3>')
        out.append('                <ul class="analysis-ul">')
        out.append('                    <li><strong>核心目標：</strong>%s</li>' % esc(m['goal']))
        out.append('                    <li><strong>主要挑戰：</strong>%s</li>' % esc(m['challenge']))
        out.append('                </ul>')
        out.append('                <h3 class="analysis-h3">關鍵工具運用（與「%s」分頁的 %d 個工具一致）：</h3>'
                   % (m['tab_label'], len(ov['tools'])))
        for fw, note in ov['tools']:
            out.append('                <div class="analysis-tool">')
            out.append('                    <strong>%s：</strong>%s' % (esc(fw), esc(note)))
            out.append('                </div>')
        out.append('            </section>')
        out.append('            ')
    out.append('            <hr class="my-10 border-slate-300">')
    out.append('            <section class="analysis-section">')
    out.append('                <h2 class="analysis-h2">%s</h2>' % esc(C.SUMMARY['heading']))
    out.append('                <ul class="analysis-ul">')
    for label, rest in C.SUMMARY['items']:
        out.append('                    <li><strong>%s</strong>%s</li>' % (esc(label), esc(rest)))
    out.append('                </ul>')
    out.append('            </section>')
    return out


def main():
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    panes = []
    for i, s in enumerate(C.STAGES):
        if i:
            panes.append('        ')
        panes += render_stage_pane(s)
    html = tpl.replace('<!--{{STAGE_PANES}}-->', '\n'.join(panes))
    html = html.replace('<!--{{OVERVIEW_SECTIONS}}-->', '\n'.join(render_overview_sections()))

    left = re.findall(r'<!--\{\{[A-Z_]+\}\}-->', html)
    if left:
        raise SystemExit('未替換的標記：%s' % left)

    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)

    ids = re.findall(r'<textarea[^>]*id="([^"]+)"', html)
    dup = sorted({x for x in ids if ids.count(x) > 1})
    print('產生 index.html：%d bytes，%d 個欄位%s' % (len(html.encode()), len(ids),
          '' if not dup else '，⚠️ 重複 id: %s' % dup))
    print('%d 個框架、%d 個階段、%d 條總覽說明'
          % (len(C.FRAMEWORKS), len(C.STAGES), sum(len(v['tools']) for v in C.OVERVIEW.values())))


if __name__ == '__main__':
    main()
