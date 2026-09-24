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
            "obj-stage": ("目前自認所處階段", "創業期／成長期／成熟期／衰退轉型期；不確定就用上面的「階段判定」。多個事業單位階段不同時，這裡寫主要對象的階段，其他單位的差異寫進⑤ BCG 各列的策略欄", ""),
            "obj-question": ("這份分析要回答的問題", "例如：要不要在第二個轉運站旁再開一間？", ""),
        },
    ),
    dict(
        key="5f", num="②", title="五力分析（產業結構）",
        desc="五力看的是「這個產業好不好賺」，不是「你贏不贏」。這是產業體檢，不是公司體檢。",
        criteria="每一力都要寫出「誰」和「他手上有多大的籌碼」：\n"
                 "　供應商議價力高＝料源集中、你換掉他的成本高、沒有替代料。\n"
                 "　客戶議價力高＝客戶集中或採購量大、他換掉你的成本低、資訊透明、有替代選擇。\n"
                 "不要寫「競爭激烈」—— 要寫「有幾家、市佔怎麼分、誰在打價格」。\n"
                 "五力全部都強＝這個產業結構天生難賺，策略要往「換產業位置」想，不是更努力。",
        example="半導體設備零件維修\n"
                "供應商議價力＝高（原廠料源單一，不能換）；客戶議價力＝中（客戶是少數大廠、集中度高，但停機成本遠高於維修費，對價格不敏感）；\n"
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
        key="vrio", num="③", title="VRIO 分析（內部資源）",
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
        key="swot", num="④", title="SWOT 分析",
        desc="SWOT 放在五力與 VRIO 之後，因為它是收斂而不是起點：S／W 從③ VRIO 歸納，O／T 從② 五力與外部變化歸納。"
             "SWOT 經常被寫成四張清單，然後就沒有然後了。它的價值在配對。",
        criteria="S／W 是自己內部的、可以改的；O／T 是外部環境、你改不動的。\n"
                 "每一條後面都要能接「所以呢？」—— 接不出來的就刪掉，那是願望不是分析。\n"
                 "真正在做決策的是配對：S×O 進攻、W×O 補強、S×T 防禦、W×T 風險（最該先處理）。",
        example="區域型停車場＋智取店\n"
                "S＝自有土地、不必付租金（但土地可以出租，機會成本＝同地段市場租金）；W＝現金流單薄，無法同時複製多點；\n"
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
        key="bcg", num="⑤", title="BCG 矩陣（事業組合）",
        desc="用兩個可觀測的變數定象限，不要憑感覺擺位置：市場成長率 × 相對市佔（你 ÷ 最大對手）。"
             "成長率「高」的基準：市場年成長約 10% 以上，或明顯高於整體經濟與產業平均。"
             "每個事業單位各填一列，下面會自動畫出位置。",
        criteria="現金流方向才是重點，不是「這事業好不好」：\n"
                 "　明星（高成長 × 高市佔）：還在吃現金，但值得投，目標是把領先變成護城河。\n"
                 "　金牛（低成長 × 高市佔）：產現金，收割它、用它養別的。\n"
                 "　問號（高成長 × 低市佔）：選擇性投資 —— 要嘛打到第一（相對市佔 ≥1），要嘛退出，不要吊著。\n"
                 "　狗（低成長 × 低市佔）：退出、轉型，或縮到只剩必要投入。\n"
                 "相對市佔 < 1 就是「不是第一」。多個單位請一起看：金牛的現金流向明星與問號，狗要想退出順序。",
        example="停車場：成長率高（轉運站啟用）、相對市佔高 → 明星（現在該投設備與動線，先拉開領先幅度）\n"
                "智取店：成長率高、相對市佔低（周邊超商取貨點較多、量較大）→ 問號（先看它能不能做到區內第一，否則只是耗資源）\n"
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
                "市場滲透＝向現有車主推月租與洗車；市場開發＝到別的轉運站旁開第二個據點（同一套服務、新地區）；\n"
                "產品開發＝加裝充電樁服務電動車；多角化＝在空地辦市集或開餐飲（新產品，客群也不是停車的人）。\n"
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
        desc="先選戰場範圍（全市場或集中一個小範圍），再選靠成本還是靠差異化贏。"
             "成本與差異化「兩種都想要」又沒有結構支撐，容易卡在中間（stuck in the middle），風險最高。",
        criteria="成本領先：你的結構成本就是比別人低（規模、自有資產、製程），所以能用價格擋人。\n"
                 "差異化：客戶願意為某個東西多付錢，而你做得到、對手做不到。\n"
                 "集中：只在一個小範圍做到前兩者之一，放棄其他市場 —— 所以選「集中」還要再選是成本集中或差異化集中。\n"
                 "成本與差異化兼得並非不可能（例如 IKEA），但前提是有結構性的理由，而不是兩邊都想要。\n\n"
                 "選定之後要看一致性：選成本領先卻在花錢做品牌，選差異化卻在砍服務成本 —— 那就是還沒選。",
        example="自有土地停車場：成本集中 —— 只在轉運站周邊這個範圍，靠不付租金把價格做低；\n"
                "但定價底線要算進土地的機會成本（租給別人能收多少），否則等於把土地收益白送給客人。\n"
                "不追求全鎮覆蓋，也不去做高價代客泊車。",
        layout=[("radio", "porter-choice", [("cost", "成本領先"), ("diff", "差異化"), ("focus", "集中")], None, "你要用哪一種？"),
                ("radio", "porter-focus-basis", [("cost", "成本集中"), ("diff", "差異化集中")], None,
                 "若選「集中」：在這個範圍內靠什麼贏？"),
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
        example="停車場：累積量＝累積服務車次。\n"
                "服務過的車次越多，排班、收費流程、尖峰疏導、糾紛處理越熟練 → 每車次需要的人力工時下降。\n"
                "注意：把固定成本攤到更多車次是規模／使用率效果，不是經驗曲線；兩者要分開看。",
        layout=[("list", ["ec-note"])],
        items={
            "ec-note": ("你累積了什麼？哪一項成本跟著降？", "沒有在累積就明說，那也是結論", ""),
        },
    ),
    dict(
        key="synth", num="⑨", title="綜合判斷",
        desc="把上面八段收斂成一頁，回頭回答①「這份分析要回答的問題」。這一頁就是你要拿去做決定的東西。",
        criteria=None, example=None,
        layout=[("list", ["synth-key", "synth-verdict"])],
        items={
            "synth-key": ("如果只能改一件事", "寫一件。寫兩件等於沒選", ""),
            "synth-verdict": ("整體判斷：①的問題，答案是什麼？", "先直接回答①的問題，再列兩三個最關鍵的依據並註明出自哪個框架（例如：五力結構、VRIO 結論、BCG 位置、SWOT 配對）", ""),
        },
    ),
]

# ── 階段判讀（隨階段變，每階段 3 欄）──────────────────────────────

STAGES = ["startup", "growth", "maturity", "decline"]

STAGE_META = {
    "startup": dict(
        tab_label="創業期", pane_title="創業期判讀",
        goal="找到可重複的商業模式（PMF）", challenge="現金流與需求驗證",
        reading="這個階段唯一該問的是「有沒有人真的要用、願不願意付錢」。所有分析都要回到這一點。",
        items={
            "read-startup-1": ("最核心的矛盾是什麼？", "例如：想驗證需求，但現金只夠撐六個月", ""),
            "read-startup-2": ("從上面的分析看，這個階段最該先做的一件事", "通常不是擴張，是把一個具體客群做透", ""),
            "read-startup-3": ("什麼訊號出現時，代表可以進入成長期？", "要有數字，不要寫「感覺穩定」", ""),
        },
    ),
    "growth": dict(
        tab_label="成長期", pane_title="成長期判讀",
        goal="把已驗證的模式規模化", challenge="規模化與資金、組織跟不上",
        reading="需求已被驗證，風險轉移到「複製得夠快嗎、品質會不會掉、現金夠不夠撐」。",
        items={
            "read-growth-1": ("最核心的矛盾是什麼？", "例如：訂單成長速度大於交付能力", ""),
            "read-growth-2": ("從上面的分析看，這個階段最該先做的一件事", "通常是補瓶頸，不是再加業績", ""),
            "read-growth-3": ("什麼訊號出現時，代表該守住而非擴張？", "例如：獲客成本連續三個月上升", ""),
        },
    ),
    "maturity": dict(
        tab_label="成熟期", pane_title="成熟期判讀",
        goal="把現金流效率最大化並找第二曲線", challenge="成長停滯、組織僵化、競爭侵蝕利潤",
        reading="重點從「成長」變成「效率與防守」，同時要開始為下一條曲線鋪路。",
        items={
            "read-maturity-1": ("最核心的矛盾是什麼？", "例如：維持服務品質的成本逐年上升，但價格漲不動", ""),
            "read-maturity-2": ("從上面的分析看，這個階段最該先做的一件事", "常見答案是砍掉低效的資源配置", ""),
            "read-maturity-3": ("第二曲線的候選是什麼？需要多少資源？", "沒有候選也要寫「還沒有」", ""),
        },
    ),
    "decline": dict(
        tab_label="衰退轉型期", pane_title="衰退轉型期判讀",
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
    "startup": ["④ SWOT 分析", "③ VRIO 分析", "② 五力分析"],
    "growth": ["⑥ 安索夫矩陣", "⑤ BCG 矩陣", "② 五力分析", "⑧ 經驗曲線"],
    "maturity": ["⑤ BCG 矩陣", "⑦ 波特基本策略", "② 五力分析", "④ SWOT 分析"],
    "decline": ["④ SWOT 分析", "⑤ BCG 矩陣", "⑥ 安索夫矩陣", "③ VRIO 分析"],
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
    title="行動計畫",
    desc="策略沒有變成「誰、在什麼時候、做到什麼數字」就只是願望。"
         "成功指標要能被外部的人驗證，不要寫「提升滿意度」這種無法否證的句子。",
    example="要做什麼：推出月租 40 席方案（限轉運站通勤族）／負責人：我自己（前期不外包）／"
            "期限：2026-12-31／成功指標：月租售出 40 席，或連續兩個月月租收入 ≥ 停車收入 30%",
)

# ── 執行與溝通（整合自「任務管理工具箱」）────────────────────────
# 欄位 id 沿用原站（tool-<n>-*），原站存在同網域 localStorage 的資料可以直接帶入，不需要對應表。
# 原站 key：TASK_TOOLKIT_KEY；主題欄 ws-topic 只在「分析對象」空白時帶入 obj-name。

TASK_TOOLKIT_KEY = "managerToday8ToolsTabsData"

EXECUTION_INTRO = dict(
    title="執行與溝通",
    desc="策略決定「做什麼」；這一頁處理怎麼拆、怎麼排、怎麼做、怎麼說、怎麼回顧。"
         "建議順序：A OGSM 把⑨的判斷拆成目標 → B 4P 落到市場 → C 艾森豪排優先 → D 5W1H 把單一事項想完整 → "
         "E SCRUM 分輪推進 → F 黃金圈、G PREP 對人說明 → H STAR 回顧成果。每一個也都可以單獨使用。",
    note="曾在「任務管理工具箱」網站存過資料的話，第一次開這個工具箱時會自動帶入這一頁（原站資料不會刪除）。",
)

EXECUTION = [
    dict(
        key="ogsm", num="A", title="OGSM（把策略拆成目標與衡量）",
        desc="把⑨綜合判斷變成一頁計畫：一個方向、幾個數字目標、達成的做法、每個做法怎麼量。",
        criteria="O 是方向，用文字、不放數字；G 是數字，要有期限，而且量的是結果（營收、市佔、滿載率），不是活動。\n"
                 "S 是選擇 —— 寫「做什麼、不做什麼」，每個 S 都要能連回某個 G；超過 3～4 個 S 就等於沒選。\n"
                 "M 分兩種：Dashboard 看 S 有沒有在推進（領先指標）；Action Plan 是有負責人與期限的具體動作。\n"
                 "常見錯誤：把動作寫成 G（「推出月租方案」是 S 或行動，不是 G）。",
        example="O＝成為轉運站周邊通勤族的首選停車點\n"
                "G＝2027 年底前月租 60 席、平日滿載率 85%\n"
                "S＝① 月租綁定通勤族（不打臨停價格戰）② 停車與智取店動線整合\n"
                "M＝Dashboard：每週月租新簽數、平日 8 點滿載率；Action Plan：12 月底前推出月租 40 席方案"
                "（細項搬到「行動計畫」分頁追蹤狀態與期限）",
        layout=[("list", ["tool-8-o", "tool-8-g", "tool-8-s"]),
                ("grid", 2, ["tool-8-m-dashboard", "tool-8-m-action"])],
        items={
            "tool-8-o": ("O（Objective）最終目的", "一句話的方向，不放數字。例如：成為轉運站周邊通勤族的首選停車點", ""),
            "tool-8-g": ("G（Goal）具體目標", "可量化、有期限的結果。例如：2027 年底前月租 60 席", ""),
            "tool-8-s": ("S（Strategy）策略", "做什麼、不做什麼；每一條連回一個 G", ""),
            "tool-8-m-dashboard": ("M：衡量指標（Dashboard）", "怎麼知道 S 有在推進？例如：每週月租新簽數", ""),
            "tool-8-m-action": ("M：行動計畫（Action Plan）", "誰、什麼時候、做什麼。要追蹤的項目搬到「行動計畫」分頁", ""),
        },
    ),
    dict(
        key="4p", num="B", title="4P 行銷組合",
        desc="把⑦選定的基本策略落到實際的產品、價格、通路、推廣。四個 P 要彼此一致，也要跟⑦一致。",
        criteria="先確認目標客群（沿用①），四個 P 都是對這群人做的選擇。\n"
                 "一致性檢查：選成本集中卻在做昂貴的推廣、選差異化卻在打折 —— 就是矛盾。\n"
                 "4P 是賣方視角；每一格也換成客戶視角檢查一次：他得到什麼價值、總共付出多少、方不方便、怎麼知道你。",
        example="客群＝轉運站通勤族\n"
                "Product＝月租固定車位＋包裹代收；Price＝月租約為臨停 30 天總額的 6 成，但不低於土地機會成本；\n"
                "Place＝現場＋LINE 預約；Promotion＝轉運站公告欄與首月優惠，不做全鎮廣告（與成本集中一致）。",
        layout=[("matrix", 2, ["tool-6-product", "tool-6-price", "tool-6-place", "tool-6-promotion"])],
        items={
            "tool-6-product": ("Product 產品", "賣什麼？核心功能與配套服務", ""),
            "tool-6-price": ("Price 價格", "定價方式、折扣、付款；底線要算進成本與機會成本", ""),
            "tool-6-place": ("Place 通路", "客戶在哪裡買到、怎麼交付", ""),
            "tool-6-promotion": ("Promotion 推廣", "客戶怎麼知道你？只寫會觸及目標客群的管道", ""),
        },
    ),
    dict(
        key="eisenhower", num="C", title="艾森豪矩陣（排優先順序）",
        desc="把手上的事依「重要」和「緊急」分四格。重要＝對目標有貢獻（對回 OGSM 的 G）；緊急＝有期限壓力。",
        criteria="「重要」要用目標檢驗，不是用感覺：對不回任何 G 或行動計畫的事，就不重要。\n"
                 "第二格（重要不緊急）才是策略真正發生的地方 —— 先排進行事曆，否則會被第一、三格吃掉。\n"
                 "第三格最會騙人：感覺很忙，其實是別人的優先。交辦時要交代要的結果與期限。\n"
                 "第一格長期爆滿，通常代表第二格的預防工作做太少。",
        example="重要且緊急：本週五前回覆轉運站管理處的租約條款\n"
                "重要不緊急：設計月租方案、訓練代班人員\n"
                "不重要但緊急：臨時的廠商推銷、非必要會議 → 交辦或婉拒\n"
                "不重要不緊急：研究別的鄉鎮的地價 → 刪掉",
        layout=[("matrix", 2, ["tool-1-q1", "tool-1-q2", "tool-1-q3", "tool-1-q4"])],
        items={
            "tool-1-q1": ("重要且緊急（馬上做）", "今天或本週一定要處理、對目標有直接影響的事", ""),
            "tool-1-q2": ("重要不緊急（排進行事曆）", "對目標有貢獻但沒人催的事 —— 寫下要排在哪一天", ""),
            "tool-1-q3": ("不重要但緊急（交辦）", "有人在催、但對你的目標沒貢獻。交給誰？", ""),
            "tool-1-q4": ("不重要不緊急（刪掉）", "可以直接不做的事", ""),
        },
    ),
    dict(
        key="5w1h", num="D", title="5W1H（把一件事想完整）",
        desc="拿行動計畫或第二格裡的一件事來拆，找出遺漏。一次只拆一件事。",
        criteria="先寫 Why：答不出為什麼要做，其他五題不必寫。\n"
                 "Who 分清楚負責人（只能一個）和參與者；When 要有日期，不是「盡快」。\n"
                 "How 寫到「下一步具體動作」為止，並把成本（How much）一起寫進去 —— 這一項最常被漏掉。",
        example="Why＝提高固定收入、避開臨停價格戰（對應 G：月租 60 席）\n"
                "What＝推出月租 40 席；Who＝我負責，家人支援現場；When＝11/15 公告、12/1 開賣；\n"
                "Where＝B 區 40 格劃為月租專區；How＝LINE 預約＋現場繳費、首月 9 折，預算 8,000 元（標線與告示）",
        layout=[("grid", 2, ["tool-3-why", "tool-3-what", "tool-3-who", "tool-3-when", "tool-3-where", "tool-3-how"])],
        items={
            "tool-3-why": ("Why 為什麼做", "連回哪一個目標？不做會怎樣？", ""),
            "tool-3-what": ("What 做什麼", "具體到別人看得懂要交出什麼", ""),
            "tool-3-who": ("Who 誰", "負責人（一個）、參與者、對象", ""),
            "tool-3-when": ("When 何時", "開始日、完成日、檢查點", ""),
            "tool-3-where": ("Where 何地", "在哪裡做、在哪裡交付", ""),
            "tool-3-how": ("How 怎麼做（含成本）", "步驟、方法、預算", ""),
        },
    ),
    dict(
        key="scrum", num="E", title="SCRUM（分輪推進）",
        desc="事情多、需求會變時，用 1～4 週為一輪推進，每輪結束都要有可以檢查的成果。不是軟體專案也能用。",
        criteria="Product Backlog 是全部想做的事，依價值排序，越上面寫得越具體。\n"
                 "Sprint Backlog 只放這一輪做得完的；一輪中途不改目標，臨時插進來的事放回 Backlog 重新排序。\n"
                 "完成的定義（DoD）要可以檢驗 —— 「客戶已經能用」，不是「做得差不多」。\n"
                 "回顧只問三件事：保留什麼、改掉什麼、下一輪要試的一個改進。一個人也能用，重點是節奏，不是儀式。",
        example="Backlog：月租方案、充電樁評估、智取店動線、夜間照明\n"
                "本輪（2 週）：月租方案上線；DoD：告示已貼、LINE 預約可用、第一位客戶完成繳費\n"
                "回顧：保留 LINE 預約；改掉現場收現金 → 下一輪改成轉帳",
        layout=[("grid", 2, ["tool-2-backlog", "tool-2-sprint", "tool-2-dod", "tool-2-retro"])],
        items={
            "tool-2-backlog": ("產品待辦清單（Product Backlog）", "全部想做的事，依價值排序", ""),
            "tool-2-sprint": ("本輪待辦（Sprint Backlog）", "這一輪（幾週？）做得完的項目與本輪目標", ""),
            "tool-2-dod": ("完成的定義（Definition of Done）", "做到什麼程度才算完成？要能檢驗", ""),
            "tool-2-retro": ("回顧（Retrospective）", "保留什麼、改掉什麼、下一輪試什麼", ""),
        },
    ),
    dict(
        key="golden", num="F", title="黃金圈（說明為什麼）",
        desc="由內而外說：先講為什麼（Why），再講怎麼做（How），最後才是做什麼（What）。用在對員工、夥伴、客戶說明方向。",
        criteria="Why 不是「賺錢」—— 賺錢是結果；Why 是你為誰解決什麼問題、為什麼在乎。\n"
                 "How 是你跟別人不一樣的做法，應該對得上③ VRIO 的核心資源；對不上，就只是口號。\n"
                 "檢查方法：把 Why 念給客戶聽，他會覺得跟自己有關嗎？\n"
                 "黃金圈是溝通框架，不是策略分析，不能取代五力或 VRIO。",
        example="Why＝讓搭客運的人不用為了停車和取包裹多繞一趟\n"
                "How＝就在轉運站旁的自有土地，一次完成停車與取件\n"
                "What＝月租／臨停車位＋蝦皮智取店",
        layout=[("list", ["tool-5-why", "tool-5-how", "tool-5-what"])],
        items={
            "tool-5-why": ("Why 為什麼", "你為誰解決什麼問題？為什麼在乎？", ""),
            "tool-5-how": ("How 怎麼做", "你跟別人不一樣的做法（對回 VRIO 的核心資源）", ""),
            "tool-5-what": ("What 做什麼", "具體提供的產品或服務", ""),
        },
    ),
    dict(
        key="prep", num="G", title="PREP（一段話講清楚）",
        desc="結論先說、給理由、舉例子、再收回結論。用在會議發言、簡報、回覆主管或客戶。",
        criteria="第一句就是結論：對方只聽第一句，也知道你要什麼。\n"
                 "理由最多三個，最有力的先講。例子要具體（數字、名字、日期），不是把理由換句話再說一次。\n"
                 "最後的 Point 要比開頭更具體，最好帶一個請求 —— 你要對方決定什麼、什麼時候前。",
        example="P＝建議 12 月推出月租 40 席\n"
                "R＝平日早上 8 點前就停滿，臨停客之間只能削價競爭；月租能鎖住固定收入\n"
                "E＝過去 4 週平日滿載率 92%，其中約 6 成是同一批通勤車\n"
                "P＝請在本週決定是否劃出 B 區 40 格，我 11/15 前公告",
        layout=[("list", ["tool-4-p1", "tool-4-r", "tool-4-e", "tool-4-p2"])],
        items={
            "tool-4-p1": ("Point 結論", "一句話說出你的主張或請求", ""),
            "tool-4-r": ("Reason 理由", "為什麼？最多三個，最有力的先講", ""),
            "tool-4-e": ("Example 例子", "具體的數字、事件、日期", ""),
            "tool-4-p2": ("Point 重申結論", "再說一次，並寫出你要對方做的決定", ""),
        },
    ),
    dict(
        key="star", num="H", title="STAR 法則（回顧成果）",
        desc="把一段經驗講成有結構的故事：情境、任務、行動、結果。用在專案復盤、成果回報、績效回顧與面試。",
        criteria="S 和 T 加起來不超過四分之一，重點放在 A 和 R。\n"
                 "A 寫「我」做了什麼：團隊做的要說清楚你的角色，而且是具體動作，不是態度。\n"
                 "R 要有數字，並對照原本的目標（可回頭對 OGSM 的 G）；沒達標也照實寫，加一句學到什麼。",
        example="S＝轉運站啟用後臨停車流大增，周邊業者開始削價\n"
                "T＝在不降價的前提下穩住收入\n"
                "A＝我把 B 區劃為月租、用 LINE 預約收單、首月 9 折\n"
                "R＝兩個月售出 38 席（目標 40），月租收入佔停車收入 34%；學到：通勤族在乎「保證有位」勝過折扣",
        layout=[("list", ["tool-7-s", "tool-7-t", "tool-7-a", "tool-7-r"])],
        items={
            "tool-7-s": ("S（Situation）情境", "當時的背景，兩三句就好", ""),
            "tool-7-t": ("T（Task）任務", "你要達成什麼？", ""),
            "tool-7-a": ("A（Action）行動", "你具體做了哪些事？", ""),
            "tool-7-r": ("R（Result）結果", "數字、對照目標、學到什麼", ""),
        },
    ),
]

# ── 輸出區 ────────────────────────────────────────────────────

OUTPUT_INTRO = dict(
    title="輸出與備份",
    desc="存檔只存在這台裝置的瀏覽器裡（localStorage）。換裝置、換瀏覽器、清快取都會不見，"
         "所以定期按「備份 JSON」留一份檔案。",
)
