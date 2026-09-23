# -*- coding: utf-8 -*-
"""內容資料 —— 唯一真實來源（v2 結構）

index.html 是產生出來的檔案，不要直接改它。改內容請改這裡，然後跑：

    bash build.sh

v2 與 v1 的差別：
  v1：7 個框架 × 各階段各一份，91 個欄位，其中約 70 個是同一批問題重填。
  v2：分析與階段無關 → 只填一次（33 欄）；階段判讀才隨階段變（每階段 3 欄）；
      行動計畫獨立（12 欄）。分析欄位 id 不再帶階段後綴。

欄位 id 就是存檔的 key，所以 ID_MIGRATION 是「舊存檔能不能搬過來」的關鍵。
"""

TITLE = "商業生命週期策略工具箱 v3"

SCHEMA_VERSION = 3

# 舊版（v1）欄位 id → v2 新欄位 id。
# 值可以是純字串，或 (標籤, 舊id) —— 有標籤者會加上「── 舊版『標籤』內容 ──」再接內容。
# 對到多個時，取第一個「有內容」的（單一目標時則全部依序附加）。
ID_MIGRATION = {
    "obj-name": ["ws-topic"],
    "swot-s": ["swot-s-startup", "swot-s-maturity", "swot-s-decline"],
    "swot-w": ["swot-w-startup", "swot-w-maturity", "swot-w-decline"],
    "swot-o": ["swot-o-maturity", "swot-o-decline"],
    "swot-t": ["swot-t-maturity", "swot-t-decline"],
    "5f-rivalry": ["5f-rivalry-startup", "5f-rivalry-growth", "5f-rivalry-maturity"],
    "5f-entrant": ["5f-entrants-startup", "5f-entrants-growth", "5f-entrants-maturity"],
    "5f-substitute": ["5f-substitutes-startup", "5f-substitutes-growth", "5f-substitutes-maturity"],
    "5f-supplier": ["5f-suppliers-startup", "5f-suppliers-growth", "5f-suppliers-maturity"],
    "5f-buyer": ["5f-buyers-startup", "5f-buyers-growth", "5f-buyers-maturity"],
    "vrio-resource": ["vrio-resource-startup", "vrio-resource-growth", "vrio-resource-maturity", "vrio-resource-decline"],
    # v1 的 vrio-v/r/i/o 是文字欄；v2 是「是/否」+ 說明欄，所以文字搬進說明欄
    "vrio-v-note": ["vrio-v-startup", "vrio-v-growth", "vrio-v-maturity", "vrio-v-decline"],
    "vrio-r-note": ["vrio-r-startup", "vrio-r-growth", "vrio-r-maturity", "vrio-r-decline"],
    "vrio-i-note": ["vrio-i-startup", "vrio-i-growth", "vrio-i-maturity", "vrio-i-decline"],
    "vrio-o-note": ["vrio-o-startup", "vrio-o-growth", "vrio-o-maturity", "vrio-o-decline"],
    "ansoff-marketpen": ["ansoff-mp-growth", "ansoff-mp-maturity", "ansoff-mp-decline"],
    "ansoff-dev": ["ansoff-md-growth", "ansoff-md-maturity", "ansoff-md-decline"],
    "ansoff-product": ["ansoff-pd-growth", "ansoff-pd-maturity", "ansoff-pd-decline"],
    "ansoff-diversify": ["ansoff-d-growth", "ansoff-d-maturity", "ansoff-d-decline"],
    "ansoff-choice": ["ansoff-priority-growth", "ansoff-priority-maturity", "ansoff-renewal-decline"],
    "bcg-1-strategy": [("明星事業 (Stars)", "bcg-stars-growth"), ("問題事業 (Question Marks)", "bcg-questions-growth"),
                       ("金牛事業 (Cash Cows)", "bcg-cows-growth"), ("狗事業 (Dogs)", "bcg-dogs-growth"),
                       ("明星事業", "bcg-stars-maturity"), ("問題事業", "bcg-questions-maturity"),
                       ("金牛事業", "bcg-cows-maturity"), ("狗事業", "bcg-dogs-maturity"),
                       ("明星事業", "bcg-stars-decline"), ("問題事業", "bcg-questions-decline"),
                       ("金牛事業", "bcg-cows-decline"), ("狗事業", "bcg-dogs-decline")],
    "porter-why": [("成本領導", "generic-cost-maturity"), ("差異化", "generic-diff-maturity"),
                   ("聚焦", "generic-focus-maturity"), ("是否陷入中間狀態", "generic-stuck-maturity")],
    "ec-note": ["ws-growth-ec"],
    # 階段判讀：v1 各階段的「策略意涵／可持續性／初步決策」就是使用者的階段結論
    "read-startup-2": [("可持續性與保護策略", "vrio-sustain-startup"), ("初步結論與進入點", "5f-conclusion-startup")],
    "read-growth-2": [("可持續性與強化策略", "vrio-sustain-growth"), ("策略意涵", "5f-implications-growth")],
    "read-maturity-2": [("可持續性與強化策略", "vrio-sustain-maturity"), ("策略意涵", "5f-implications-maturity"),
                        ("SWOT 策略意涵", "swot-implications-maturity")],
    "read-decline-2": [("所需的新 VRIO 資源／能力", "vrio-gap-decline"), ("初步決策", "swot-decision-decline")],
}

# v2 → v3：BCG 從「單一事業單位」改為多個（bcg-<n>-*），舊欄位平移為第 1 個單位。
ID_MIGRATION_V2 = {
    "bcg-1-unit": ["bcg-unit"],
    "bcg-1-growth": ["bcg-growth"],
    "bcg-1-share": ["bcg-share"],
    "bcg-1-strategy": ["bcg-strategy"],
}

# ── ①～⑨ 分析區（填一次，與階段無關）─────────────────────────────

ANALYSIS = [
    dict(
        key="obj", num="①", title="對象與現況",
        desc="先把「在分析什麼」寫清楚。這一段含糊，後面每一個框架都會跟著含糊。",
        criteria=None, example=None,
        layout=[("grid", 2, ["obj-name", "obj-offer"]),
                ("grid", 2, ["obj-industry", "obj-customers"]),
                ("grid", 2, ["obj-scale", "obj-stage"]),
                ("list", ["obj-question"])],
        items={
            "obj-name": ("公司／產品／專案名稱", "例如：埔里轉運站旁停車場＋蝦皮智取店", ""),
            "obj-offer": ("提供什麼（一句話）", "用一句話說清楚你賣什麼、解決誰的什麼問題", ""),
            "obj-industry": ("產業與市場範圍", "例如：南投埔里鎮、轉運站周邊 500 公尺", ""),
            "obj-customers": ("主要客群", "誰付錢？誰使用？兩個可能不是同一群人", ""),
            "obj-scale": ("目前規模", "營收／人數／據點數／月流量，用你手上有的數字", ""),
            "obj-stage": ("目前自認所處階段", "創業期／成長期／成熟期／衰退轉型期；不確定就用上面的「階段判讀」", ""),
            "obj-question": ("這份分析要回答的問題", "例如：要不要在第二個轉運站旁再開一間？", ""),
        },
    ),
    dict(
        key="swot", num="②", title="SWOT 分析",
        desc="SWOT 經常被寫成四張清單，然後就沒有然後了。它的價值在配對。",
        criteria="S／W 是自己內部的、可以改的；O／T 是外部環境、你改不動的。\n"
                 "每一條後面都要能接「所以呢？」—— 接不出來的就刪掉，那是願望不是分析。\n"
                 "真正在做決策的是配對：S×O 進攻、W×O 補強、S×T 防禦、W×T 風險（最該先處理）。",
        example="區域型停車場＋智取店\n"
                "S＝自有土地、零租金成本；W＝現金流單薄，無法同時複製多點；\n"
                "O＝轉運站啟用後每日人流可望翻倍；T＝周邊業者跟進價格戰。\n"
                "配對：S×O 用零租金優勢撐過前期低載客；W×T 若價格戰開打，沒有第二個據點攤提成本 —— 這是最該先處理的一格。",
        layout=[("matrix", 2, ["swot-s", "swot-w", "swot-o", "swot-t"])],
        items={
            "swot-s": ("優勢 (S)", "內部的、別人拿不走的。問「對手要花多久才能追上？」", "內部"),
            "swot-w": ("劣勢 (W)", "內部可改的。不要寫「資源不足」這種沒有指向的答案", "內部"),
            "swot-o": ("機會 (O)", "外部正在發生、對你有利的變化。要有時間點", "外部"),
            "swot-t": ("威脅 (T)", "外部正在發生、對你不利的變化。要有時間點", "外部"),
        },
    ),
    dict(
        key="5f", num="③", title="五力分析（產業結構）",
        desc="五力看的是「這個產業好不好賺」，不是「你贏不贏」。這是產業體檢，不是公司體檢。",
        criteria="每一力都要寫出「誰」和「他手上有多大的籌碼」：\n"
                 "　議價力高的訊號＝來源單一、轉換成本低、資訊透明、有替代選擇。\n"
                 "不要寫「競爭激烈」—— 要寫「有幾家、市佔怎麼分、誰在打價格」。\n"
                 "五力全部都強＝這個產業結構天生難賺，策略要往「換產業位置」想，不是更努力。",
        example="半導體設備零件維修\n"
                "供應商議價力＝高（原廠料源單一，不能換）；客戶議價力＝低（停機成本遠高於維修費）；\n"
                "替代品＝低（沒有等效替代）；新進入者＝低（技術認證門檻）；同業競爭＝中（三家寡佔、不打價格）。\n"
                "結論：結構好賺，護城河來自轉換成本而不是價格。",
        layout=[("list", ["5f-rivalry", "5f-entrant", "5f-substitute", "5f-supplier", "5f-buyer"])],
        items={
            "5f-rivalry": ("現有競爭者", "幾家？市佔怎麼分？主要在打價格還是打差異？", ""),
            "5f-entrant": ("新進入者的威脅", "他進來要花多久、多少錢？有沒有執照／認證／通路門檻？", ""),
            "5f-substitute": ("替代品的威脅", "客戶「不買你的」還能怎麼解決同一件事？", ""),
            "5f-supplier": ("供應商的議價力", "你的料源有幾家？換一家要多久？", ""),
            "5f-buyer": ("客戶的議價力", "客戶集中度？他換掉你要付出什麼？", ""),
        },
    ),
    dict(
        key="vrio", num="④", title="VRIO 分析（內部資源）",
        desc="VRIO 是四道關卡，不是四個形容詞。四題一路問下去，會得到四種結論之一。",
        criteria="V 價值性：這項資源能不能讓你提高售價、降低成本，或擋掉一個威脅？\n"
                 "R 稀有性：現在有幾個對手也有？\n"
                 "I 難以模仿：對手要花多久、多少錢才能複製？（不是「很難」，是「大約多久」）\n"
                 "O 組織運用：你有沒有流程、人才、獎酬制度真的在用它？\n\n"
                 "　V 否 → 競爭劣勢（這不是資源，是負擔）\n"
                 "　V 是、R 否 → 競爭均勢（人人都有的門檻）\n"
                 "　V 是、R 是、I 否 → 暫時優勢（領先，但要一直往前跑）\n"
                 "　V 是、R 是、I 是、O 否 → 未利用的潛力（有牌不會打，問題出在組織）\n"
                 "　四項皆為是 → 持續優勢（這才是護城河）",
        example="自有土地上的既有停車場\n"
                "V＝是（同地段替代品租金高，價格有空間）；R＝是（同地段土地不止一塊，但可出租的不多）；\n"
                "I＝否（對手持現金也能買地，約 1～2 年就能複製）→ 結論：暫時優勢。\n"
                "策略含義：趁領先期把客戶關係與動線體驗做深，讓下一個對手進來時已經來不及。",
        layout=[("list", ["vrio-resource"]),
                ("radio", "vrio-v", [("yes", "是"), ("no", "否")], "vrio-v-note"),
                ("radio", "vrio-r", [("yes", "是"), ("no", "否")], "vrio-r-note"),
                ("radio", "vrio-i", [("yes", "是"), ("no", "否")], "vrio-i-note"),
                ("radio", "vrio-o", [("yes", "是"), ("no", "否")], "vrio-o-note"),
                ("verdict", "vrio")],
        items={
            "vrio-resource": ("要檢驗的核心資源／能力", "一次一項。有多項就複製這一組再做一次", ""),
            "vrio-v-note": ("V：憑什麼說有價值？", "連到具體的價格、成本或風險", ""),
            "vrio-r-note": ("R：有幾個對手也有？", "寫出數量或名字", ""),
            "vrio-i-note": ("I：對手要多久才能複製？", "用時間和金錢回答，不要寫「很難」", ""),
            "vrio-o-note": ("O：組織真的在用它嗎？", "有沒有流程、負責人、獎酬在支撐", ""),
        },
    ),
    dict(
        key="bcg", num="⑤", title="BCG 矩陣（事業組合）",
        desc="用兩個可觀測的變數定象限，不要憑感覺擺位置：市場成長率 × 相對市佔（你 ÷ 最大對手）。"
             "每個事業單位各填一列，下面會自動畫出位置。",
        criteria="現金流方向才是重點，不是「這事業好不好」：\n"
                 "　明星（高成長 × 高市佔）：還在吃現金，但值得投，目標是把領先變成護城河。\n"
                 "　金牛（低成長 × 高市佔）：產現金，收割它、用它養別的。\n"
                 "　問號（高成長 × 低市佔）：選擇性投資 —— 要嘛打進前三，要嘛退出，不要吊著。\n"
                 "　狗（低成長 × 低市佔）：退出、轉型，或縮到只剩必要投入。\n"
                 "相對市佔 < 1 就是「不是第一」。多個單位請一起看：金牛的現金流向明星與問號，狗要想退出順序。",
        example="停車場：成長率高（轉運站啟用）、相對市佔高 → 明星（現在該投設備與動線，先拉開領先幅度）\n"
                "智取店：成長率高、相對市佔低（蝦皮自有品牌在旁）→ 問號（先看它能不能進前三，否則只是耗資源）\n"
                "洗車：成長率低、市佔高 → 金牛（不要加投資，用它的現金養別的事業）",
        layout=[("bcgmatrix", None)],
        items={},
    ),
    dict(
        key="ansoff", num="⑥", title="安索夫矩陣（成長方向）",
        desc="「現有／新」產品 ×「現有／新」市場，四個格子。風險由低到高：滲透 → 市場開發 → 產品開發 → 多角化。",
        criteria="資源有限時，預設答案是「先榨乾市場滲透」，不是直接跳到多角化。\n"
                 "只有當現有市場明顯做不動了（成長率趨零、客戶飽和），才往下一格走。\n"
                 "多角化是最貴的一格：你要同時學新產品和新市場 —— 除非有明確理由，否則它通常是逃生而不是策略。",
        example="停車場＋智取店\n"
                "市場滲透＝向現有車主推月租與洗車；市場開發＝把智取店服務推給轉運站乘客；\n"
                "產品開發＝加裝充電樁服務電動車；多角化＝到別的鄉鎮開第二個據點（同時是新市場與新營運模式）。\n"
                "主戰場：市場滲透 —— 邊際成本最低，先做。",
        layout=[("matrix", 2, ["ansoff-marketpen", "ansoff-dev", "ansoff-product", "ansoff-diversify"]),
                ("list", ["ansoff-choice"])],
        items={
            "ansoff-marketpen": ("市場滲透（現有產品 × 現有市場）", "怎麼讓現有客戶買更多／來更頻繁？", ""),
            "ansoff-dev": ("市場開發（現有產品 × 新市場）", "同一套東西還能賣給誰？", ""),
            "ansoff-product": ("產品開發（新產品 × 現有市場）", "現有客戶還需要什麼、你順手做得到？", ""),
            "ansoff-diversify": ("多角化（新產品 × 新市場）", "最貴的一格。寫之前先問「為什麼非做不可」", ""),
            "ansoff-choice": ("主戰場：先打哪一格？為什麼？", "通常答案是市場滲透 —— 除非你有明確理由", ""),
        },
    ),
    dict(
        key="porter", num="⑦", title="波特基本策略",
        desc="三種策略只能選一種。「兩種都做」的結果是卡在中間（stuck in the middle），通常最慘。",
        criteria="成本領先：你的結構成本就是比別人低（規模、自有資產、製程），所以能用價格擋人。\n"
                 "差異化：客戶願意為某個東西多付錢，而你做得到、對手做不到。\n"
                 "集中：只在一個小範圍做到前兩者之一，放棄其他市場。\n\n"
                 "選定之後要看一致性：選成本領先卻在花錢做品牌，選差異化卻在砍服務成本 —— 那就是還沒選。",
        example="自有土地停車場：偏向「集中」—— 只在轉運站周邊這個範圍，用零租金做到最低價；\n"
                "不追求全鎮覆蓋，也不去做高價代客泊車。",
        layout=[("radio", "porter-choice", [("cost", "成本領先"), ("diff", "差異化"), ("focus", "集中")], None, "你要用哪一種？"),
                ("list", ["porter-why"])],
        items={
            "porter-why": ("為什麼選這個？資源配置要怎麼一致？", "寫出「所以我會把錢花在…、不花在…」", ""),
        },
    ),
    dict(
        key="ec", num="⑧", title="經驗曲線",
        desc="累積產量每翻一倍，單位成本會下降一個固定比例。重點是「你有沒有在累積」，不是「你有沒有比對手便宜」。",
        criteria="有用的問法：過去一年你的累積產量／服務量翻倍了嗎？有沒有哪一項成本跟著下降？\n"
                 "如果你的量沒在長，經驗曲線對你就是靜止的 —— 那代表你的優勢只能靠別的東西。\n"
                 "反向用法：對手量比你大，他的成本就會持續比你低，價格戰你打不贏。",
        example="停車場：車位數固定，累積量＝累積服務車次。\n"
                "推月租讓固定車主佔比提高 → 每日周轉次數上升 → 每車次分攤的人力與清潔成本下降。",
        layout=[("list", ["ec-note"])],
        items={
            "ec-note": ("你累積了什麼？哪一項成本跟著降？", "沒有在累積就明說，那也是結論", ""),
        },
    ),
    dict(
        key="synth", num="⑨", title="綜合判斷",
        desc="把上面八段收斂成一頁。這一頁就是你要拿去做決定的東西。",
        criteria=None, example=None,
        layout=[("list", ["synth-key", "synth-verdict"])],
        items={
            "synth-key": ("如果只能改一件事", "寫一件。寫兩件等於沒選", ""),
            "synth-verdict": ("整體判斷", "把 SWOT 配對、五力結構、VRIO 結論串成一句話", ""),
        },
    ),
]

# ── 階段判讀（隨階段變，每階段 3 欄）──────────────────────────────

STAGES = ["startup", "growth", "maturity", "decline"]

STAGE_META = {
    "startup": dict(
        tab_label="創業期", pane_title="🌱 創業／導入期判讀",
        goal="找到可重複的商業模式（PMF）", challenge="現金流與需求驗證",
        reading="這個階段唯一該問的是「有沒有人真的要用、願不願意付錢」。所有分析都要回到這一點。",
        items={
            "read-startup-1": ("最核心的矛盾是什麼？", "例如：想驗證需求，但現金只夠撐六個月", ""),
            "read-startup-2": ("從上面的分析看，這個階段最該先做的一件事", "通常不是擴張，是把一個具體客群做透", ""),
            "read-startup-3": ("什麼訊號出現時，代表可以進入成長期？", "要有數字，不要寫「感覺穩定」", ""),
        },
    ),
    "growth": dict(
        tab_label="成長期", pane_title="🚀 成長期判讀",
        goal="把已驗證的模式規模化", challenge="規模化與資金、組織跟不上",
        reading="需求已被驗證，風險轉移到「複製得夠快嗎、品質會不會掉、現金夠不夠撐」。",
        items={
            "read-growth-1": ("最核心的矛盾是什麼？", "例如：訂單成長速度大於交付能力", ""),
            "read-growth-2": ("從上面的分析看，這個階段最該先做的一件事", "通常是補瓶頸，不是再加業績", ""),
            "read-growth-3": ("什麼訊號出現時，代表該守住而非擴張？", "例如：獲客成本連續三個月上升", ""),
        },
    ),
    "maturity": dict(
        tab_label="成熟期", pane_title="🌳 成熟期判讀",
        goal="把現金流效率最大化並找第二曲線", challenge="成長停滯、組織僵化、競爭侵蝕利潤",
        reading="重點從「成長」變成「效率與防守」，同時要開始為下一條曲線鋪路。",
        items={
            "read-maturity-1": ("最核心的矛盾是什麼？", "例如：維持服務品質的成本逐年上升，但價格漲不動", ""),
            "read-maturity-2": ("從上面的分析看，這個階段最該先做的一件事", "常見答案是砍掉低效的資源配置", ""),
            "read-maturity-3": ("第二曲線的候選是什麼？需要多少資源？", "沒有候選也要寫「還沒有」", ""),
        },
    ),
    "decline": dict(
        tab_label="衰退/轉型期", pane_title="🍂 衰退／轉型期判讀",
        goal="優雅退出或找到第二曲線轉型", challenge="決策退出 vs. 轉型、重新配置資源",
        reading="這個階段最大的風險不是衰退本身，是「拖」—— 拖著做不出決定，資源會自己流光。",
        items={
            "read-decline-1": ("最核心的矛盾是什麼？", "例如：轉型需要投入，但現金流正在萎縮", ""),
            "read-decline-2": ("從上面的分析看，這個階段最該先做的一件事", "通常是設停損點，不是再試一次", ""),
            "read-decline-3": ("退出或轉型的決定點是什麼？（時間／數字）", "要可驗證，例如：Q2 前月租未達 40 位即退出", ""),
        },
    ),
}

# 階段判讀時，這個階段最該回頭看的分析（唯讀提示，不重複填）
STAGE_READING_TOOLS = {
    "startup": ["② SWOT 分析", "④ VRIO 分析", "③ 五力分析"],
    "growth": ["⑥ 安索夫矩陣", "⑤ BCG 矩陣", "③ 五力分析", "⑧ 經驗曲線"],
    "maturity": ["⑤ BCG 矩陣", "⑦ 波特基本策略", "③ 五力分析", "② SWOT 分析"],
    "decline": ["② SWOT 分析", "⑤ BCG 矩陣", "⑥ 安索夫矩陣", "④ VRIO 分析"],
}

# ── 行動計畫 ──────────────────────────────────────────────────

ACTION_ROWS = 4

BCG_MAX_UNITS = 6
BCG_DEFAULT_UNITS = 3
BCG_UNIT_FIELDS = [("unit", "事業單位名稱", "例如：停車場、智取店、洗車"),
                   ("strategy", "對應策略（由象限推出）", "先看自動判定的象限，再寫你要做什麼")]
BCG_GROWTH_OPTIONS = [("hi", "高"), ("lo", "低")]
BCG_SHARE_OPTIONS = [("hi", "高（≥1）"), ("lo", "低（<1）")]
BCG_QUADRANTS = [("star", "明星", "高成長 × 高市佔"), ("question", "問號", "高成長 × 低市佔"),
                 ("cow", "金牛", "低成長 × 高市佔"), ("dog", "狗", "低成長 × 低市佔")]
ACTION_FIELDS = [("what", "要做什麼"), ("owner", "負責人"), ("due", "期限"), ("metric", "成功指標")]

# 每項行動的狀態（下拉；會存檔）
ACTION_STATUS = [("todo", "未開始"), ("doing", "進行中"), ("done", "已完成"), ("drop", "已取消")]

ACTION_INTRO = dict(
    title="🎯 行動計畫",
    desc="策略沒有變成「誰、在什麼時候、做到什麼數字」就只是願望。"
         "成功指標要能被外部的人驗證，不要寫「提升滿意度」這種無法否證的句子。",
    example="要做什麼：推出月租 40 席方案（限轉運站通勤族）／負責人：我自己（前期不外包）／"
            "期限：2026-12-31／成功指標：月租售出 40 席，或連續兩個月月租收入 ≥ 停車收入 30%",
)

# ── 輸出區 ────────────────────────────────────────────────────

OUTPUT_INTRO = dict(
    title="📤 輸出與備份",
    desc="存檔只存在這台裝置的瀏覽器裡（localStorage）。換裝置、換瀏覽器、清快取都會不見，"
         "所以定期按「備份 JSON」留一份檔案。",
)
