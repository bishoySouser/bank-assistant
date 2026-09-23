import streamlit as st
from langchain_core.messages import HumanMessage
from src.agent import create_cib_agent

st.set_page_config(
    page_title="CIB AI Assistant",
    page_icon="🏦",
    layout="centered"
)

# تخصيص الواجهة
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 CIB AI Smart Assistant")
st.caption("الجيل القادم من المساعد المصرفي الذكي - مدعوم بالذكاء الاصطناعي التوليدي والـ RAG")

@st.cache_resource
def load_agent():
    return create_cib_agent()

agent_executor = load_agent()

# إدارة الرسائل التفاعلية
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
    st.session_state.ui_messages = [
        {"role": "assistant", "content": "أهلاً بك في البنك التجاري الدولي (CIB) 🇪🇬\nكيف يمكنني مساعدتك اليوم بخصوص الشهادات، البطاقات الائتمانية، أو القروض الشخصية؟"}
    ]

# استخراج النص الصافي من رد النموذج
def extract_text_from_response(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        full_text = ""
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                full_text += item.get("text", "")
            elif isinstance(item, str):
                full_text += item
        return full_text if full_text else str(content)
    return str(content)

# عرض الرسائل في الواجهة
for msg in st.session_state.ui_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إدخال العميل
if prompt := st.chat_input("اكتب استفسارك هنا (مثال: احسبلي عائد شهادة بريميوم)..."):
    st.session_state.ui_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري التحقق من الأنظمة المصرفية..."):
            try:
                # تمرير سجل المحادثة للـ Agent للحفاظ على سياق الحوار
                st.session_state.chat_messages.append(HumanMessage(content=prompt))
                response = agent_executor.invoke({"messages": st.session_state.chat_messages})
                
                last_msg = response["messages"][-1]
                st.session_state.chat_messages.append(last_msg)
                
                clean_reply = extract_text_from_response(last_msg.content)
                st.markdown(clean_reply)
                st.session_state.ui_messages.append({"role": "assistant", "content": clean_reply})

            except Exception as e:
                error_alert = f"حدث خطأ غير متوقع: {str(e)}"
                st.error(error_alert)