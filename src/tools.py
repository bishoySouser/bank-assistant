from langchain.tools import tool

@tool
def calculate_loan_installment(principal: float, duration_months: int, annual_interest_rate: float = 0.22) -> str:
    """
    حساب القسط الشهري التقريبي للقرض الشخصي وإجمالي المبلغ المستحق.
    المدخلات:
    - principal: أصل مبلغ القرض بالجنيه (مثال: 100000)
    - duration_months: مدة السداد بالشهور (مثال: 12, 24, 36)
    - annual_interest_rate: الفائدة السنوية المتناقصة (افتراضياً 0.22 أي 22%)
    """
    if principal <= 0 or duration_months <= 0:
        return "خطأ: قيمة القرض ومدة السداد يجب أن تكون أرقاماً موجبة."

    # حساب تقريبي للفائدة والقسط الشهري
    years = duration_months / 12
    total_interest = principal * annual_interest_rate * years
    total_payable = principal + total_interest
    monthly_installment = total_payable / duration_months

    return (
        f"تفاصيل الحسبة التقديرية للقرض:\n"
        f"- أصل المبلغ: {principal:,.2f} جنيه مصري\n"
        f"- مدة السداد: {duration_months} شهر ({int(years)} سنة)\n"
        f"- الفائدة السنوية المطبقة: {annual_interest_rate * 100:.1f}%\n"
        f"- القسط الشهري المتوقع: {monthly_installment:,.2f} جنيه مصري\n"
        f"- إجمالي المبلغ الواجب سداده: {total_payable:,.2f} جنيه مصري."
    )

@tool
def freeze_card_emergency(last_four_digits: str, card_type: str = "debit") -> str:
    """
    إجراء أمني طارئ لإيقاف بطاقة بنكية مفقودة أو مسروقة مؤقتاً فوراً.
    المدخلات:
    - last_four_digits: آخر 4 أرقام من البطاقة فقط (مثال: '4321')
    - card_type: نوع البطاقة ('debit' أو 'credit')
    """
    if len(last_four_digits) != 4 or not last_four_digits.isdigit():
        return "خطأ أمني: يرجى تزويدنا بآخر 4 أرقام من البطاقة فقط للتأكيد."

    return (
        f"🚨 تم بنجاح الإيقاف المؤقت الفوري للبطاقة ({card_type}) "
        f"المنتهية بالأرقام **** {last_four_digits}.\n"
        f"تم إرسال رسالة تأكيد إلى هاتفك المسجل لدى البنك التجاري الدولي (CIB). "
        f"إذا لم تكن قد طلبت هذا الإجراء، يرجى الاتصال فوراً بالخط الساخن 19666."
    )

@tool
def calculate_certificate_roi(amount: float, cd_type: str = "premium") -> str:
    """
    حساب العائد الشهري للشهادات الادخارية الثلاثية في CIB.
    المدخلات:
    - amount: المبلغ المراد استثماره بالجنيه
    - cd_type: نوع الشهادة ('premium', 'plus', 'prime')
    """
    cd_rates = {
        "premium": {"rate": 0.22, "min": 1_000_000, "name": "شهادة بريميوم الثلاثية"},
        "plus": {"rate": 0.21, "min": 500_000, "name": "شهادة بلس الثلاثية"},
        "prime": {"rate": 0.20, "min": 100_000, "name": "شهادة برايم الثلاثية"}
    }
    
    cd_key = cd_type.lower()
    if cd_key not in cd_rates:
        return "نوع الشهادة غير معروف. الأنواع المتاحة: premium (22%), plus (21%), prime (20%)."

    selected_cd = cd_rates[cd_key]
    
    if amount < selected_cd["min"]:
        return (
            f"الحد الأدنى لشراء {selected_cd['name']} هو {selected_cd['min']:,.2f} جنيه. "
            f"المبلغ المدخل ({amount:,.2f}) غير كافٍ."
        )

    annual_return = amount * selected_cd["rate"]
    monthly_return = annual_return / 12

    return (
        f"عوائد {selected_cd['name']}:\n"
        f"- مبلغ الاستثمار: {amount:,.2f} جنيه مصري\n"
        f"- نسبة العائد السنوي الثابت: {selected_cd['rate'] * 100:.1f}%\n"
        f"- العائد الشهري الذي سيصرف لحسابك: {monthly_return:,.2f} جنيه مصري\n"
        f"- إجمالي العائد خلال 3 سنوات: {annual_return * 3:,.2f} جنيه مصري."
    )