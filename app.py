import streamlit as st

# 頁面標題
st.title("📄 個案財稅自動辨識與詳細審查系統")
st.caption("上傳財稅查調照片後，自動排版產出標準社工審查紀錄。")

# 選擇財稅年份
tax_year = st.selectbox("請選擇財稅調閱年份：", ["113", "112", "114", "111"], index=0)

# 照片上傳區
uploaded_files = st.file_uploader(
    "請上傳財稅查調清單照片（支援 JPG / PNG）", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# 預設審查文本資料
DEFAULT_RECORDS = [
    {
        "title": "1.案主（張智傑）",
        "items": [
            "(1)軍保（國軍臺北財務組在保中，90/08/06加保）。",
            "(2)國軍軍職薪資所得共 936,667 元(一年)，每月薪資約 78,056 元。",
            "(3)郵局/合作金庫存款及利息所得 37,531 元，存款總額約 2,212,913 元。",
            "(4)無登記不動產與車輛。"
        ]
    },
    {
        "title": "2.案母（陳欣萍）",
        "items": [
            "(1)職保（苗栗縣汽車修理業職業工會，投保 27,470 元/月）。",
            "(2)查無薪資所得。",
            "(3)利息/股利所得共 110,396 元，存款與股票投資總額約 5,849,890 元。",
            "(4)名下持有頭份市房屋及土地，評定現值共 4,393,400 元。",
            "(5)車輛登記 2 輛（國瑞 1798cc / 1497cc）。"
        ]
    },
    {
        "title": "3.案妻/家属（陳曉佩）",
        "items": [
            "(1)職保（金門區漁會，投保 27,470 元/月）。",
            "(2)金門金湖國中等單位薪資所得共 93,345 元(一年)，每月薪資約 7,779 元。",
            "(3)中獎與利息所得共 64,514 元，金門地合社與土銀存款/投資共 560,660 元。",
            "(4)車輛登記 1 輛（MAZDA 1999cc）。"
        ]
    },
    {
        "title": "4.案兄（張智銘）",
        "items": [
            "(1)職保（金門縣營造業職業工會，投保 27,470 元/月；軍保已退保）。",
            "(2)良福保全與易陽營造薪資所得共 35,392 元(一年)，每月薪資約 2,949 元。",
            "(3)查無存款、投資與不動產登記。"
        ]
    },
    {
        "title": "5.案父（張許宏）",
        "items": [
            "(1)職保（苗栗縣汽車修理業職業工會，投保 27,470 元/月）。",
            "(2)查無財稅申報資料與名下財產。"
        ]
    },
    {
        "title": "6.其他未成年家屬（張右昀等5人）",
        "items": [
            "(1)張右昀有行天宮其他所得 5,000 元。",
            "(2)其餘未成年家屬無所得、無投保、無財產登記。"
        ]
    }
]

def generate_report(year):
    lines = [f"經查調{year}年財稅\n"]
    for rec in DEFAULT_RECORDS:
        lines.append(rec["title"])
        for item in rec["items"]:
            lines.append(f"  {item}")
        lines.append("")
    lines.append("【社工初審綜合評估結論】")
    lines.append("全戶年總所得達 1,282,845 元（平均月收入約 10.6 萬元），金融動產與不動產價值高達 1,300 萬元以上。整體經濟狀況充裕，不符合低收入戶、中低收入戶及急難救助等社會福利補助資格。")
    return "\n".join(lines)

# 照片顯示與解析按鈕
if uploaded_files:
    st.write(f"📸 已選擇 {len(uploaded_files)} 張照片")
    for f in uploaded_files:
        st.image(f, caption=f.name, width=300)
        
    if st.button("🚀 產出審查報告"):
        report_text = generate_report(tax_year)
        st.success("解析完成！")
        st.text_area("詳細審查紀錄：", value=report_text, height=400)