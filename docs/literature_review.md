# 文獻探討（完整版 v1）
情境化AI決策支援對智慧製造管理者資訊理解、信任與決策採用意願之影響

---

## 2.1 人機信任理論脈絡

信任是使用者是否依賴自動化或AI建議的核心前提。Muir (1987) 最早提出人機信任的概念模型，指出信任程度會直接決定使用者對自動化系統的依賴行為。Mayer, Davis 與 Schoorman (1995) 提出組織信任整合模型，將信任拆解為能力（ability）、誠信（integrity）、善意（benevolence）三個構面，此架構後續被廣泛延伸至人機信任與AI信任研究。

Lee 與 See (2004) 提出「自動化信任」（trust in automation）的經典框架，主張信任程度決定使用者是否能「適當依賴」（appropriate reliance）自動化建議——過度信任會導致過度依賴（over-reliance），信任不足則會導致系統效益無法發揮（under-reliance / disuse）。Hoff 與 Bashir (2015) 進一步統整實證證據，將信任區分為三個層次：傾向性信任（dispositional trust，使用者個人特質決定的基礎信任傾向）、情境性信任（situational trust，隨任務與情境而變化）、習得性信任（learned trust，隨使用經驗累積而調整）。此三層次架構說明信任並非靜態特質，而會隨系統呈現的資訊內容動態變化——這正是本研究以「情境化程度」作為自變項的理論依據。

近年研究進一步聚焦於「信任校準」（trust calibration）議題，即如何讓使用者的信任程度與系統實際可靠度相符，而非單純提高信任。McGuirl 與 Sarter (2006) 的經典研究發現，呈現動態系統信心資訊（dynamic system confidence information）能有效協助使用者校準信任並更恰當地使用決策輔助工具——此發現直接支持本研究原型中「AI建議信心水準」欄位的設計。Schemmer, Kuehl, Benz, Bartos 與 Satzger (2023) 則指出，解釋（explanation）對信任與依賴行為的影響並非單純的正向線性關係，其效果會因解釋呈現的形式與使用者的專業背景而異。Naiseh, Al-Thani, Jiang 與 Ali (2023) 針對臨床決策支援系統的研究也發現，不同類別的解釋方式（explanation classes）對信任校準的影響存在顯著差異，說明「情境化資訊」的呈現形式本身即是值得操作化並實證檢驗的變項。Vereschak, Bailly 與 Caramiaux (2021) 系統性回顧AI輔助決策中信任的實證量測方法，指出多數研究仍以單一量表題項量測信任，缺乏將信任量測與實際決策行為並列驗證的研究設計——此一方法缺口也是本研究採用「行為資料＋量表資料」雙軌設計的直接依據。

## 2.2 技術接受模式與資訊系統成功理論

Davis (1989) 提出的技術接受模式（Technology Acceptance Model, TAM）主張，知覺有用性（perceived usefulness）與知覺易用性（perceived ease of use）是決定使用者採用新科技行為意圖的兩大核心前因。TAM自提出以來已成為資訊系統採用研究中最廣泛應用的理論框架之一，本研究以「決策採用意願」對應TAM的行為意圖構面。

DeLone 與 McLean (1992, 2003) 提出的資訊系統成功模式（IS Success Model）則主張，資訊品質（information quality）與系統品質（system quality）會影響使用者的「使用」與「使用者滿意度」，進而產生淨效益（net benefits）。本研究以「情境化AI決策資訊品質」對應此模式中的資訊品質構面——亦即AI建議所附帶的證據來源、風險分級、信心水準等資訊完整度，是否足以支撐管理者做出高品質的判斷。

Goodhue 與 Thompson (1995) 提出的任務科技適配理論（Task-Technology Fit, TTF）主張，科技工具唯有與使用者的任務需求相符，才能真正提升使用績效；適配程度低的科技，即便功能先進，仍可能因不符合任務脈絡而遭使用者棄用或誤用。本研究以TTF觀點檢視「異常升級決策」此一高複雜度、高時間壓力任務，與「AI建議呈現形式」（情境化 vs. 一般結論式）之間的適配性，作為感知決策品質構面的理論基礎。

## 2.3 智慧製造與AI決策支援現況

全球製造業對AI的投資與導入持續加速，但根據Deloitte（2025）針對600位製造業高階主管的年度調查，人才與組織信任仍是智慧製造推行的首要障礙，技術可行性反而已非主要瓶頸——此發現凸顯「組織與行為面」議題（而非純技術議題）在AI決策支援導入中的關鍵地位。

然而，現有AI決策支援的實證研究仍高度集中於醫療臨床決策情境（clinical decision support），Tun, Rahman, Naing 與 Malik (2025) 針對醫療工作者信任AI-CDSS的系統性回顧即涵蓋27篇文獻，反映此一子領域的研究密度。相較之下，聚焦製造業管理者決策情境的實證研究相對稀少。Marocco, Barbieri 與 Talamo (2024) 針對「管理者採用AI系統進行決策」的障礙與促進因素進行系統性回顧，指出多數既有研究聚焦技術效能本身，較少實證探討管理者如何與AI建議互動、如何形成信任並轉化為實際決策行為。Montealegre-López (2025) 系統性回顧70篇AI驅動決策中信任角色的文獻後，依「決策增強」（augmented decision-making，AI提供建議、人類決定）與「決策自動化」（automated decision-making，AI獨立決策）兩大類型進行分類，發現「決策增強」情境下的信任研究仍屬分散、缺乏整合型實證模型——本研究的實驗設計（AI僅提供建議、由管理者做最終決策）即屬於此一決策增強情境，直接呼應此研究缺口。

## 2.4 研究定位與理論整合

綜合上述文獻可歸納三項缺口：（1）理論缺口——信任理論多在自動化系統與醫療臨床決策情境中驗證，較少延伸至製造業管理者的異常升級決策；（2）方法缺口——多數研究以問卷量測「採用意願」，鮮少同時蒐集「實際決策行為」資料；（3）情境缺口——「情境化AI建議」是否比單純結論式建議更能建立信任與理解，目前尚缺乏對照實驗證據。

本研究整合信任理論（Trust in Automation）、技術接受模式（TAM）、資訊系統成功理論（IS Success Model）、任務科技適配理論（TTF）四個理論脈絡，並援引信任校準（trust calibration）文獻中「動態信心資訊」與「解釋類別」的實證發現，作為「情境化AI決策資訊品質」此一自變項的操作化依據。研究設計上，本研究以行為資料（實際決策、耗時）與量表資料（四構念、Likert量表）雙軌驗證，回應Vereschak等人（2021）指出的方法缺口，期能為製造業管理決策情境下的AI信任研究提供實證補充。

---

## 參考文獻（含DOI，已逐筆查證真實存在）

Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly*, *13*(3), 319–340. https://doi.org/10.2307/249008

Deloitte. (2025). *2025 Smart Manufacturing and Operations Survey: Navigating challenges to implementation*. Deloitte Insights. https://www.deloitte.com/us/en/insights/industry/manufacturing/2025-smart-manufacturing-survey.html

DeLone, W. H., & McLean, E. R. (1992). Information systems success: The quest for the dependent variable. *Information Systems Research*, *3*(1), 60–95. https://doi.org/10.1287/isre.3.1.60

DeLone, W. H., & McLean, E. R. (2003). The DeLone and McLean model of information systems success: A ten-year update. *Journal of Management Information Systems*, *19*(4), 9–30. https://doi.org/10.1080/07421222.2003.11045748

Goodhue, D. L., & Thompson, R. L. (1995). Task-technology fit and individual performance. *MIS Quarterly*, *19*(2), 213–236. https://doi.org/10.2307/249689

Hoff, K. A., & Bashir, M. (2015). Trust in automation: Integrating empirical evidence on factors that influence trust. *Human Factors*, *57*(3), 407–434. https://doi.org/10.1177/0018720814547570

Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. *Human Factors*, *46*(1), 50–80. https://doi.org/10.1518/hfes.46.1.50_30392

Marocco, S., Barbieri, B., & Talamo, A. (2024). Exploring facilitators and barriers to managers' adoption of AI-based systems in decision making: A systematic review. *AI*, *5*(4), 2538–2567. https://doi.org/10.3390/ai5040123 （開放取用）

Mayer, R. C., Davis, J. H., & Schoorman, F. D. (1995). An integrative model of organizational trust. *Academy of Management Review*, *20*(3), 709–734. https://doi.org/10.5465/amr.1995.9508080335

McGuirl, J. M., & Sarter, N. B. (2006). Supporting trust calibration and the effective use of decision aids by presenting dynamic system confidence information. *Human Factors*, *48*(4), 656–665. https://doi.org/10.1518/001872006779166334

Montealegre-López, N. (2025). Exploring the role of trust in AI-driven decision-making: A systematic literature review. *Management Review Quarterly*. https://doi.org/10.1007/s11301-025-00526-4

Muir, B. M. (1987). Trust between humans and machines, and the design of decision aids. *International Journal of Man-Machine Studies*, *27*(5-6), 527–539. https://doi.org/10.1016/S0020-7373(87)80013-5

Naiseh, M., Al-Thani, D., Jiang, N., & Ali, R. (2023). How the different explanation classes impact trust calibration: The case of clinical decision support systems. *International Journal of Human-Computer Studies*, *169*, 102941. https://doi.org/10.1016/j.ijhcs.2022.102941

Schemmer, M., Kuehl, N., Benz, C., Bartos, A., & Satzger, G. (2023). Appropriate reliance on AI advice: Conceptualization and the effect of explanations. In *Proceedings of the 28th International Conference on Intelligent User Interfaces* (IUI '23) (pp. 410–422). ACM. https://doi.org/10.1145/3581641.3584066

Tun, H. M., Rahman, H. A., Naing, L., & Malik, O. A. (2025). Trust in artificial intelligence–based clinical decision support systems among health care workers: Systematic review. *Journal of Medical Internet Research*, *27*, e69678. https://doi.org/10.2196/69678 （開放取用）

Vereschak, O., Bailly, G., & Caramiaux, B. (2021). How to evaluate trust in AI-assisted decision making? A survey of empirical methodologies. *Proceedings of the ACM on Human-Computer Interaction*, *5*(CSCW2), 1–39. https://doi.org/10.1145/3476068 （開放取用，HAL: hal-03280969）

---

*每筆文獻已於2026/8以搜尋逐一核對作者、年份、期刊、卷期頁碼與DOI，詳細查證記錄見 `reference_verification.md`。*

---

*本版本涵蓋四大理論脈絡的核心與近三年重要延伸文獻，共16篇。正式論文文獻探討章節建議依委員意見進一步擴充至30-50篇規模，並補充台灣/亞太地區製造業AI導入的在地實證研究（如有）。*
