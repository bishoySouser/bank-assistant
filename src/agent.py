import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain.tools import tool

from src.rag import get_retriever
from src.tools import (
    calculate_loan_installment,
    freeze_card_emergency,
    calculate_certificate_roi
)

load_dotenv()

# تحميل مسترجع قاعدة المعرفة
retriever = get_retriever()

@tool
def cib_knowledge_base(query: str) -> str:
    """ابحث في الوثائق الرسمية للبنك التجاري الدولي (CIB) بخصوص المنتجات، أنواع الشهادات، مزايا الكروت، الشروط العامة ومواعيد العمل."""
    docs = retriever.invoke(query)
    if not docs:
        return "لم يتم العثور على معلومات تطابق هذا الاستفسار في الوثائق المتاحة."
    return "\n\n".join([doc.page_content for doc in docs])

def create_cib_agent():
    tools = [
        cib_knowledge_base,
        calculate_loan_installment,
        freeze_card_emergency,
        calculate_certificate_roi
    ]

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    system_prompt = (
        "أنت المساعد الذكي الرسمي للبنك التجاري الدولي مصر (CIB Next-Gen AI Assistant).\n"
        "أنت تعمل في بيئة مصرفية رسمية وتلتزم بالمعايير التالية بدقة:\n\n"
        "1. النطاق المصرفي: مهمتك تقتصر فقط على تقديم المساعدة لعملاء CIB. "
        "إذا سُئلت عن أي موضوع خارج النطاق المالي والمصرفي، اعتذر بأدب واشرح تخصصك.\n"
        "2. الأمان والخصوصية: لا تطلب أبداً بيانات حساسة مثل الرقم السري (PIN) أو CVV. لإيقاف البطاقة نطلب آخر 4 أرقام فقط.\n"
        "3. دقة الحسابات: لا تقم بأي عمليات حسابية للقروض أو أرباح الشهادات من تلقاء نفسك، بل استخدم دائماً الأدوات المخصصة.\n"
        "4. المعرفة الرسمية: لأي استفسار عن المنتجات استخدم أداة 'cib_knowledge_base'.\n"
        "5. أسلوب الحوار: مهذب، احترافي، ومباشر باللغة العربية أو الإنجليزية حسب لغة العميل."
    )

    agent_graph = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )
    return agent_graph

if __name__ == "__main__":
    agent = create_cib_agent()
    test_query = "عايز اعرف تفاصيل شهادة بريميوم لو معايا مليون جنيه؟"
    print(f"\nالسؤال: {test_query}\n")
    
    events = agent.invoke({"messages": [HumanMessage(content=test_query)]})
    last_message = events["messages"][-1]
    print("\nالإجابة:\n", last_message.content)