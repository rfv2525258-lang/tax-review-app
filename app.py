import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# 1. 頁面標題與設定
st.set_page_config(page_title="個案財稅自動辨識系統", layout="wide")
st.title("📄 個案財稅自動辨識與詳細審查系統")
st.caption("上傳財稅查調照片後，自動排版產出標準社工審查紀錄。")

# 2. 設定 Gemini API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = genai.Client()

# 3. 選擇財稅年份
tax_year = st.selectbox("請選擇財稅調閱年份：", ["113", "112", "114", "111"], index=0)

# 4. 照片上傳區
uploaded_files = st.file_uploader(
    "請上傳財稅查調清單照片（支援 JPG / PNG）", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# 5. 照片顯示與辨識解析
if uploaded_files:
    st.write(f"📸 已選擇 {len(uploaded_files)} 張照片")
    
    # 讀取 PIL Image 物件以供顯示與模型輸入
    images = [Image.open(f) for f in uploaded_files]
    
    # 顯示上傳的照片縮圖
    cols = st.columns(min(len(images), 4))
    for idx, img in enumerate(images):
        with cols[idx % 4]:
            st.image(img, caption=uploaded_files[idx].name, use_container_width=True)
            
    if st.button("🚀 開始辨識照片並產出審查報告", type="primary"):
        with st.spinner("AI 正在辨識財稅照片內容並生成報告，請稍候..."):
            try:
                # 建立給 AI 的提示詞（Prompt）
                prompt = f"""
你是一位專業的社會工作師，請幫忙分析上傳的{tax_year}年度財稅查調清單照片。

請按照以下格式輸出標準的「個案財稅詳細審查紀錄」：

經查調{tax_year}年財稅：

【一、財稅細項列出】
請仔細辨識照片中的每一位案主/家屬姓名、身分證字號或稱謂，並依序列出其：
1. 投保/勞健保資訊（例如加保單位、日期）
2. 所得明細（例如薪資所得、股利所得、營利所得等，含金額與單位）
3. 金融動產（例如郵局/銀行存款、存款利息等，含金額）
4. 不動產與車輛（例如土地、房屋、汽車等公告現值或登記狀況）

【二、社工初審綜合評估結論】
根據上述辨識出的實際數據，進行以下評估：
1. 計算全戶年總所得與平均月收入。
2. 統計金融動產與不動產總估值。
3. 評估其整體經濟狀況，並說明是否符合低收入戶、中低收入戶或急難救助等社會福利補助資格建議。
"""

                # 組合傳送內容（提示詞 + 所有圖片）
                contents_list = [prompt] + images

                # 呼叫 Gemini Vision 模型
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents_list
                )

                st.success("解析完成！")
                st.text_area("詳細審查紀錄（可直接複製）：", value=response.text, height=500)

            except Exception as e:
                st.error(f"辨識失敗，請確認 API 設定或圖片清晰度。錯誤訊息: {e}")
