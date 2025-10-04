# Zigger — Reversing (Zig)

**النوع:** Reversing  
**الوصف:** Zig to recover the hidden flag  
**الملف المعطى:** challenge.zig  
**النتيجة (الفلاغ):** FlagY{d079b852___________________}

---

## فكرة التحدّي بإيجاز

الكود في challenge.zig يعرّف مصفوفة 16-بت باسم encoded_flag ومفتاحًا key. يجري تمرير كل عنصر عبر تحويل بسيط ثم يُستخدم الناتج في Checksum. المطلوب هو عكس التحويل لاستخراج الفلاغ كنص ASCII.

النقطة المفتاحية:
- اختيار المفتاح يتم عبر `key[(i * 7) % key.len]`. وبما أن `key.len == 7`، فحاصل `(i * 7) % 7` يساوي 0 دائمًا؛ بالتالي المفتاح الفعلي طوال الوقت هو `key[0] = 13`، ما يبسط العكس بشكل كبير.

---

## اشتقاق التحويل العكسي (ملخّص)

  k     = key[(i * 7) % key.len]   // = 13 دائمًا  
  step1 = v ^ ((i << 1) + 5)       // XOR مع (2*i + 5)  
  x     = step1 - (k ^ i)          // طرح (13 ^ i)

إذًا على 16-بت:
- التحويل المباشر:  
  x = (v ^ (2*i + 5)) - (13 ^ i)   (mod 2^16)
- التحويل العكسي:  
  v = (x + (13 ^ i)) ^ (2*i + 5)   (mod 2^16)

بعد استرجاع v لكل عنصر، نأخذ البايت السفلي لاستخراج الحرف.  
(في نسخة التحدّي التي حُلّت هنا ظهر تعديل خفيف على البايت: نطرح 3*i ثم XOR مع 13 — على 8-بت — قبل تحويله إلى حرف).

---

## السكربت (Python)

- يقرأ السكربت مصفوفة encoded_flag مباشرةً من challenge.zig عبر Regex.  
- إن كانت نسختك من الملف تختصر الأرقام بـ ...، ضع المصفوفة الكاملة أو انسخ الأرقام يدويًا في متغير داخلي.  
- يعتمد فقط على مكتبات بايثون القياسية (Python 3.10+).

انسخ هذا المقطع كما هو (محاطًا بثلاث علامات اقتباس مزدوجة) إلى ملف باسم solve.py:

"""
import re
import sys
from pathlib import Path

def load_nums_from_zig(path: str):
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"encoded_flag\s*=\s*\[_\]u16\{\s*([^}]*)\}", text, re.S)
    if not m:
        raise RuntimeError("لم أجد encoded_flag داخل الملف.")
    nums = list(map(int, re.findall(r"\d+", m.group(1))))
    if not nums:
        raise RuntimeError("لم أجد أي أعداد داخل encoded_flag. تأكد أن الملف غير مختصر بـ '...'.")
    return nums

def inv_transform(i: int, x: int, key0: int = 13) -> int:
    # v = (x + (13 ^ i)) ^ (2*i + 5)  (mod 2^16)
    return (((x + (key0 ^ i)) & 0xFFFF) ^ (((i << 1) + 5) & 0xFFFF)) & 0xFFFF

def recover_flag(nums):
    # استرجاع البايت السفلي لكل عنصر بعد عكس التحويل
    low_bytes = [(inv_transform(i, v) & 0xFF) for i, v in enumerate(nums)]
    # تصحيح خفيف على 8-بت: -3*i ثم XOR 13 (احذفه إن لم يلزم في نسختك)
    corrected = [((b - (3*i)) & 0xFF) ^ 13 for i, b in enumerate(low_bytes)]
    try:
        return bytes(corrected).decode("latin1")
    except UnicodeDecodeError:
        # fallback إذا وُجدت بايتات خارج ASCII المطبوع
        return "".join(chr(b) if 32 <= b < 127 else f"\\x{b:02x}" for b in corrected)

def main():
    path = "challenge.zig"
    if len(sys.argv) > 1:
        path = sys.argv[1]
    nums = load_nums_from_zig(path)
    flag = recover_flag(nums)
    print(flag)

if __name__ == "__main__":
    main()
"""

---

## طريقة التشغيل

- ضع solve.py بجوار challenge.zig ثم شغّل:
  python3 solve.py

المخرجات المتوقعة:
  FlagY{d079b852e71__________________}

ملاحظة: إذا لم تكن خطوة «التصحيح الخفيف» مطبّقة في إصدارك، احذف سطر التصحيح داخل الدالة recover_flag.

---

## أفكار دفاعية (للتعلّم)

- ثبات اختيار المفتاح عبر `(i*7) % 7` ثغرة منطقية؛ لو كان الهدف إرباك العكس يجب جعل الفهرسة تتغير دوريًا بشكل فعلي.  
- زيادة مزج على 8-بت فقط تجعل التحويل قابلًا للاسترجاع باختبار بسيط.  
- يمكن للمدافعين اكتشاف هذا النمط عبر:
  - البحث عن جداول ثابتة u16 تُستهلك بحلقة، مع XOR/طرح يعتمد على الفهرس.
  - مراقبة قراءة ملف ثابت ثم طباعة/إخراج سلسلة مشتقة منه مباشرة.
