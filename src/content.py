# -*- coding: utf-8 -*-
"""內容資料 —— 唯一真實來源。

index.html 是產生出來的檔案，不要直接改它。改內容請改這裡，然後跑：

    bash build.sh

新增一個框架 = 在 FRAMEWORKS 加一筆，再到 STAGE_ORDER 對應的階段加進去。
欄位 id 由 f"{item_key}-{stage}" 自動產生，不要手寫 —— 手寫會漂移，舊存檔就載不回來。
"""

STAGES = ["startup", "growth", "maturity", "decline"]

STAGE_META = {
    "startup": {
        "pane_title": "🌱 創業/導入期",
        "tab_label": "創業期",
        "goal": "存活、驗證商業模式、尋找產品市場契合度 (PMF)",
        "challenge": "資源有限、市場認知度低、高度不確定性、驗證可行性",
        # 跨階段沿用按鈕（對應 index.html 的 CARRY_MAP，改這裡要同步改那段）
        "carry_from": None,
        "carry_label_from": None,
        "carry_tools": None,
    },
    "growth": {
        "pane_title": "🚀 成長期",
        "tab_label": "成長期",
        "goal": "有效擴張規模、爭奪市場份額、建立品牌與競爭護城河",
        "challenge": "管理擴張複雜性、應對激烈競爭、保持高速成長",
        # 跨階段沿用按鈕（對應 index.html 的 CARRY_MAP，改這裡要同步改那段）
        "carry_from": "startup",
        "carry_label_from": "創業/導入期",
        "carry_tools": "VRIO、波特五力",
    },
    "maturity": {
        "pane_title": "🌳 成熟期",
        "tab_label": "成熟期",
        "goal": "維持利潤與市佔率、提升效率、尋找新成長動能",
        "challenge": "應對激烈競爭、管理客戶關係、克服組織僵化",
        # 跨階段沿用按鈕（對應 index.html 的 CARRY_MAP，改這裡要同步改那段）
        "carry_from": "growth",
        "carry_label_from": "成長期",
        "carry_tools": "波特五力、BCG、安索夫、VRIO",
    },
    "decline": {
        "pane_title": "🍂 衰退/轉型期",
        "tab_label": "衰退/轉型期",
        "goal": "優雅退出或尋找「第二曲線」實現轉型",
        "challenge": "決策退出 vs. 轉型、重新配置資源、管理變革阻力",
        # 跨階段沿用按鈕（對應 index.html 的 CARRY_MAP，改這裡要同步改那段）
        "carry_from": "maturity",
        "carry_label_from": "成熟期",
        "carry_tools": "SWOT、BCG、安索夫、VRIO",
    },
}

FRAMEWORKS = {
    "SWOT 分析": {
        "id_prefix": "swot",
        "stages": {
            "startup": {
                "title": "SWOT 分析",
                "desc": "評估初始內部與外部條件",
                "layout": [("grid", ["swot-s", "swot-w", "swot-o", "swot-t"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "swot-s": ("優勢 (Strengths)", "例如：團隊背景、技術能力、獨特洞察...", ""),
                    "swot-w": ("劣勢 (Weaknesses)", "例如：資金限制、經驗不足、資源限制...", ""),
                    "swot-o": ("機會 (Opportunities)", "例如：市場空白、新趨勢、政策支持...", ""),
                    "swot-t": ("威脅 (Threats)", "例如：潛在競爭者、法規不明、技術風險...", ""),
                },
            },
            "maturity": {
                "title": "SWOT 分析（重新評估）",
                "desc": "定期檢視變化",
                "layout": [("grid", ["swot-s", "swot-w", "swot-o", "swot-t"]), ("single", ["swot-implications"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "swot-s": ("優勢 (S)", "我們的優勢是否仍然穩固？", ""),
                    "swot-w": ("劣勢 (W)", "新的劣勢？", ""),
                    "swot-o": ("機會 (O)", "新的機會？", ""),
                    "swot-t": ("威脅 (T)", "破壞性威脅？", ""),
                    "swot-implications": ("策略意涵：", "應該強化、優化、轉型還是準備轉型？", ""),
                },
            },
            "decline": {
                "title": "SWOT 分析",
                "desc": "冷靜評估情況：退出還是轉型",
                "layout": [("grid", ["swot-s", "swot-w", "swot-o", "swot-t"]), ("single", ["swot-decision"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "swot-s": ("優勢 (S)", "有哪些優勢可轉移到新領域？", ""),
                    "swot-w": ("劣勢 (W)", "哪些劣勢加速了衰退？", ""),
                    "swot-o": ("機會 (O)", "是否有真正的轉型機會？", ""),
                    "swot-t": ("威脅 (T)", "導致衰退的威脅是否不可逆？", ""),
                    "swot-decision": ("初步決策：", "傾向於收割/退出還是轉型/重生？", ""),
                },
            },
        },
    },
    "VRIO 框架": {
        "id_prefix": "vrio",
        "stages": {
            "startup": {
                "title": "VRIO 框架",
                "desc": "識別早期獨特且可防守的優勢",
                "layout": [("single", ["vrio-resource"]), ("grid", ["vrio-v", "vrio-r", "vrio-i", "vrio-o"]), ("single", ["vrio-sustain"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "vrio-resource": ("識別核心資源/能力：", "列出潛在的早期優勢（例如：創辦人洞察、專利、特殊管道...）", ""),
                    "vrio-v": ("價值性 (Value)", "是否有助於把握機會或中和威脅？能否創造客戶價值？", ""),
                    "vrio-r": ("稀缺性 (Rarity)", "有多少競爭者擁有這項資源？", ""),
                    "vrio-i": ("難以模仿性 (Imitability)", "競爭者模仿的成本是否很高？", ""),
                    "vrio-o": ("組織性 (Organization)", "公司是否有組織來利用此資源？", ""),
                    "vrio-sustain": ("可持續性與保護策略：", "基於 VRIO 分析，我們的持續優勢是什麼？如何保護/強化？", ""),
                },
            },
            "growth": {
                "title": "VRIO 框架",
                "desc": "重新評估並強化優勢的可持續性",
                "layout": [("single", ["vrio-resource"]), ("grid", ["vrio-v", "vrio-r", "vrio-i", "vrio-o"]), ("single", ["vrio-sustain"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "vrio-resource": ("識別核心資源/能力：", "列出成長期間建立的關鍵優勢", ""),
                    "vrio-v": ("價值性 (Value)", "是否有助於把握機會或中和威脅？", ""),
                    "vrio-r": ("稀缺性 (Rarity)", "有多少競爭者擁有這項資源？", ""),
                    "vrio-i": ("難以模仿性 (Imitability)", "競爭者模仿的成本是否很高？", ""),
                    "vrio-o": ("組織性 (Organization)", "公司是否有組織來利用此資源？", ""),
                    "vrio-sustain": ("可持續性與強化策略：", "如何持續強化並防止侵蝕？", ""),
                },
            },
            "maturity": {
                "title": "VRIO 框架",
                "desc": "確保核心資源的可持續性",
                "layout": [("single", ["vrio-resource"]), ("grid", ["vrio-v", "vrio-r", "vrio-i", "vrio-o"]), ("single", ["vrio-sustain"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "vrio-resource": ("識別核心資源/能力：", "列出我們競爭所依賴的核心優勢", ""),
                    "vrio-v": ("價值性 (V)", "這項資源是否仍有價值？", ""),
                    "vrio-r": ("稀缺性 (R)", "是否仍然稀缺？", ""),
                    "vrio-i": ("難以模仿性 (I)", "對手是否已模仿？", ""),
                    "vrio-o": ("組織性 (O)", "組織是否仍能有效利用？", ""),
                    "vrio-sustain": ("可持續性與強化策略：", "如何維持或重塑 VRIO 特性？", ""),
                },
            },
            "decline": {
                "title": "VRIO 框架（轉型焦點）",
                "desc": "盤點可轉移資源並規劃新資源",
                "layout": [("single", ["vrio-resource"]), ("grid", ["vrio-v", "vrio-r", "vrio-i", "vrio-o"]), ("single", ["vrio-gap"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "vrio-resource": ("識別可轉移的核心資源/能力：", "哪些現有 VRIO 資源可轉移到新領域？", ""),
                    "vrio-v": ("價值性（在新領域）", "在新領域中是否有價值？", ""),
                    "vrio-r": ("稀缺性（在新領域）", "在新領域中是否稀缺？", ""),
                    "vrio-i": ("難以模仿性（在新領域）", "在那裡是否難以模仿？", ""),
                    "vrio-o": ("組織性（為新領域）", "組織能否適應以新方式利用它？", ""),
                    "vrio-gap": ("所需的新 VRIO 資源/能力：", "轉型成功需要哪些「新」VRIO 資源？如何獲得？", ""),
                },
            },
        },
    },
    "波特五力分析": {
        "id_prefix": "5f",
        "stages": {
            "startup": {
                "title": "波特五力分析",
                "desc": "評估基本市場吸引力",
                "layout": [("grid", ["5f-entrants", "5f-buyers", "5f-suppliers", "5f-substitutes", "5f-rivalry"]), ("single", ["5f-conclusion"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "5f-entrants": ("新進入者威脅", "進入這個市場容易嗎？", ""),
                    "5f-buyers": ("買方議價能力", "早期客戶是否有很多選擇？", ""),
                    "5f-suppliers": ("供應商議價能力", "關鍵供應商是否稀缺或強勢？", ""),
                    "5f-substitutes": ("替代品威脅", "是否有其他方式滿足客戶需求？", ""),
                    "5f-rivalry": ("競爭強度", "誰是直接對手？他們強大嗎？", ""),
                    "5f-conclusion": ("初步結論與進入點：", "基於五力分析，這個市場有吸引力嗎？什麼進入點可以避開最大壓力？", ""),
                },
            },
            "growth": {
                "title": "波特五力分析",
                "desc": "深度分析產業結構與競爭動態",
                "layout": [("grid", ["5f-entrants", "5f-buyers", "5f-suppliers", "5f-substitutes", "5f-rivalry"]), ("single", ["5f-implications"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "5f-entrants": ("新進入者威脅", "進入障礙有多高？如何提高？", ""),
                    "5f-buyers": ("買方議價能力", "如何降低買方力量？", ""),
                    "5f-suppliers": ("供應商議價能力", "如何降低供應商力量？", ""),
                    "5f-substitutes": ("替代品威脅", "如何與替代品競爭？", ""),
                    "5f-rivalry": ("競爭強度", "如何脫穎而出？", ""),
                    "5f-implications": ("策略意涵：", "應採取哪些防守或進攻行動？", ""),
                },
            },
            "maturity": {
                "title": "波特五力分析",
                "desc": "監控激烈競爭並尋找降低競爭強度的方法",
                "layout": [("grid", ["5f-entrants", "5f-buyers", "5f-suppliers", "5f-substitutes", "5f-rivalry"]), ("single", ["5f-implications"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "5f-entrants": ("新進入者威脅", "進入障礙是否仍然有效？", ""),
                    "5f-buyers": ("買方議價能力", "如何提升忠誠度/轉換成本？", ""),
                    "5f-suppliers": ("供應商議價能力", "供應商格局有何變化？", ""),
                    "5f-substitutes": ("替代品威脅", "替代品是否變得更有吸引力？", ""),
                    "5f-rivalry": ("競爭強度", "如何避免價格戰？", ""),
                    "5f-implications": ("策略意涵：", "如何在成熟市場中維持獲利能力？", ""),
                },
            },
        },
    },
    "安索夫矩陣": {
        "id_prefix": "ansoff",
        "stages": {
            "growth": {
                "title": "安索夫矩陣",
                "desc": "系統性思考成長路徑與資源配置",
                "layout": [("grid", ["ansoff-mp", "ansoff-pd", "ansoff-md", "ansoff-d"]), ("single", ["ansoff-priority"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "ansoff-mp": ("市場滲透", "如何向現有市場銷售更多現有產品？", ""),
                    "ansoff-pd": ("產品開發", "如何向現有市場銷售新產品？", ""),
                    "ansoff-md": ("市場開發", "如何向新市場銷售現有產品？", ""),
                    "ansoff-d": ("多角化", "是否應進入新產品/市場領域？", ""),
                    "ansoff-priority": ("主要成長引擎與資源配置：", "我們的主要成長引擎是什麼？資源應如何配置？", ""),
                },
            },
            "maturity": {
                "title": "安索夫矩陣",
                "desc": "尋找新成長機會",
                "layout": [("grid", ["ansoff-mp", "ansoff-pd", "ansoff-md", "ansoff-d"]), ("single", ["ansoff-priority"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "ansoff-mp": ("市場滲透", "是否還有滲透空間？", ""),
                    "ansoff-pd": ("產品開發", "向現有客戶銷售新產品的機會？", ""),
                    "ansoff-md": ("市場開發", "能否將現有產品帶到新市場？", ""),
                    "ansoff-d": ("多角化", "是否該考慮多角化？", ""),
                    "ansoff-priority": ("主要新成長向量：", "最可行的新成長路徑是什麼？", ""),
                },
            },
            "decline": {
                "title": "安索夫矩陣（轉型焦點）",
                "desc": "考慮全新的產品/市場組合",
                "layout": [("grid", ["ansoff-mp", "ansoff-pd", "ansoff-md", "ansoff-d"]), ("single", ["ansoff-renewal"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "ansoff-mp": ("市場滲透", "（通常在此階段不相關）", ""),
                    "ansoff-pd": ("產品開發", "透過新產品轉型的機會？", ""),
                    "ansoff-md": ("市場開發", "能否將產品帶到新市場？", ""),
                    "ansoff-d": ("多角化", "進入哪個新產品/市場？", ""),
                    "ansoff-renewal": ("「第二曲線」選擇：", "最可行的轉型路徑是什麼？", ""),
                },
            },
        },
    },
    "BCG 矩陣": {
        "id_prefix": "bcg",
        "stages": {
            "growth": {
                "title": "BCG 矩陣",
                "desc": "評估事業單位並配置資源",
                "layout": [("grid", ["bcg-stars", "bcg-questions", "bcg-cows", "bcg-dogs"]), ("single", ["bcg-implications"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "bcg-stars": ("明星事業 (Stars)", "列出「明星」事業與策略", "(高成長、高市佔)"),
                    "bcg-questions": ("問題事業 (Question Marks)", "列出「問題」事業與策略", "(高成長、低市佔)"),
                    "bcg-cows": ("金牛事業 (Cash Cows)", "列出「金牛」事業與策略", "(低成長、高市佔)"),
                    "bcg-dogs": ("狗事業 (Dogs)", "列出「狗」事業與策略", "(低成長、低市佔)"),
                    "bcg-implications": ("資源配置意涵：", "現金流應如何在各單位間流動？", ""),
                },
            },
            "maturity": {
                "title": "BCG 矩陣",
                "desc": "管理「金牛」事業以資助新投資",
                "layout": [("grid", ["bcg-stars", "bcg-questions", "bcg-cows", "bcg-dogs"]), ("single", ["bcg-implications"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "bcg-stars": ("明星事業", "是否還有剩餘的「明星」？", "(高成長、高市佔)"),
                    "bcg-questions": ("問題事業", "是否有新的「問題」？", "(高成長、低市佔)"),
                    "bcg-cows": ("金牛事業", "如何最大化現金流？", "(低成長、高市佔)"),
                    "bcg-dogs": ("狗事業", "策略為何？", "(低成長、低市佔)"),
                    "bcg-implications": ("資源配置意涵：", "「金牛」資金應流向何處？", ""),
                },
            },
            "decline": {
                "title": "BCG 矩陣",
                "desc": "識別並管理「狗」事業",
                "layout": [("grid", ["bcg-stars", "bcg-questions", "bcg-cows", "bcg-dogs"]), ("single", ["bcg-implications"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "bcg-stars": ("明星事業", "是否還有剩餘？", "(高成長、高市佔)"),
                    "bcg-questions": ("問題事業", "是否還有剩餘？", "(高成長、低市佔)"),
                    "bcg-cows": ("金牛事業", "是否還有現金流可收割？", "(低成長、高市佔)"),
                    "bcg-dogs": ("狗事業", "哪些是「狗」？策略為何？", "(低成長、低市佔)"),
                    "bcg-implications": ("資源退出策略：", "如何退出「狗」事業？如何最大化殘值？", ""),
                },
            },
        },
    },
    "經驗曲線": {
        "id_prefix": "ws",
        "stages": {
            "growth": {
                "title": "經驗曲線",
                "desc": "考慮成本優勢與定價策略",
                "layout": [("bare", ["ws-ec"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "ws-ec": ("", "經驗曲線效應是否顯著？是否應使用策略定價？", ""),
                },
            },
        },
    },
    "波特基本策略": {
        "id_prefix": "generic",
        "stages": {
            "maturity": {
                "title": "波特基本策略",
                "desc": "定義核心競爭策略，避免「中間狀態」",
                "layout": [("grid", ["generic-cost", "generic-diff", "generic-focus"]), ("single", ["generic-stuck"])],
                # key: (標籤, 提示文字, 標籤後的小字說明)
                "items": {
                    "generic-cost": ("成本領導", "如何在整個價值鏈中降低成本？", ""),
                    "generic-diff": ("差異化", "差異化的基礎是什麼？是否可持續？", ""),
                    "generic-focus": ("聚焦", "聚焦於哪個利基？", ""),
                    "generic-stuck": ("是否陷入「中間狀態」？", "我們的策略是否清晰？", ""),
                },
            },
        },
    },
}

STAGE_ORDER = {
    "startup": ["SWOT 分析", "VRIO 框架", "波特五力分析"],
    "growth": ["安索夫矩陣", "波特五力分析", "BCG 矩陣", "經驗曲線", "VRIO 框架"],
    "maturity": ["波特五力分析", "波特基本策略", "BCG 矩陣", "安索夫矩陣", "SWOT 分析", "VRIO 框架"],
    "decline": ["SWOT 分析", "BCG 矩陣", "安索夫矩陣", "VRIO 框架"],
}

OVERVIEW = {
    "startup": {
        "heading": "🌱 1. 創業/導入期",
        "tools": [
            ("SWOT 分析", "快速評估初始內部條件（優勢/劣勢）與外部環境（機會/威脅），建立基準認知。"),
            ("VRIO 框架", "問「我們為什麼會贏？」是否擁有獨特、難以模仿的資源？識別並保護早期優勢。"),
            ("波特五力分析", "初步評估目標市場的吸引力，幫助選擇初始進入點。"),
        ],
    },
    "growth": {
        "heading": "🚀 2. 成長期",
        "tools": [
            ("安索夫矩陣", "系統性思考成長路徑，指導資源配置。"),
            ("波特五力分析", "深度分析產業結構，制定競爭策略。"),
            ("BCG 矩陣", "評估多事業單位，決定資源分配。"),
            ("經驗曲線", "累積產量帶來的單位成本下降，決定成本優勢與定價空間。"),
            ("VRIO 框架", "重新檢視成長期新增的優勢，是否仍具價值、稀缺、難以模仿且有組織支撐。"),
        ],
    },
    "maturity": {
        "heading": "🌳 3. 成熟期",
        "tools": [
            ("波特五力分析", "監控激烈競爭，找出降低競爭強度的著力點。"),
            ("波特基本策略", "明確核心戰略，避免陷入「中間狀態」。"),
            ("BCG 矩陣", "管理「金牛」事業以資助新投資。"),
            ("安索夫矩陣", "在成長趨緩時尋找新的成長向量。"),
            ("SWOT 分析", "定期重新檢視內外部條件的變化。"),
            ("VRIO 框架", "確保核心資源在競爭對手的追趕下仍可持續。"),
        ],
    },
    "decline": {
        "heading": "🍂 4. 衰退/轉型期",
        "tools": [
            ("SWOT 分析", "評估轉型可能性，決定退出或重生。"),
            ("BCG 矩陣", "識別並管理「狗」事業，決定資源退出順序。"),
            ("安索夫矩陣", "考慮全新產品/市場組合的多角化。"),
            ("VRIO 框架", "盤點哪些資源可轉移到新領域，並規劃還缺什麼。"),
        ],
    },
}

# 「策略分析」分頁最下方的總結
SUMMARY = {
    "heading": "✨ 總結與提醒",
    "items": [
        ("工具靈活性：", "各工具在不同階段都有用，只是側重點不同"),
        ("非線性路徑：", "生命週期可能跳躍、停滯或逆轉"),
        ("情境為王：", "工具選擇永遠取決於具體情境"),
        ("適應力至上：", "基於快速反饋的適應性策略才是王道"),
    ],
}

# 欄位 id 不符 f"{key}-{stage}" 慣例者。保留原名以維持既有存檔相容，不要改。
ID_OVERRIDES = {
    "ws-ec": "ws-growth-ec",
}
