
# Hail Mary — Writeup (Challenge 3)

---

## TL;DR
التحدي كان عبارة عن واجهة خدمة تقبل **مجموعات جينات** (100 عينات × 10 أرقام عائمة 0..1) وتُقيِّم "متوسط البقاء" لنسل Taumoeba. المطلوب: خلال 100 جيل الوصول إلى متوسط 95% أو الحصول على العلم إن ظهر في استجابة الخادم.

الاستراتيجية العملية الفعّالة كانت: **بحث عشوائي منظم + hillclimb مع تبريد تباين الطفرات + تعدد محاولات (restarts) + تنقيح محلي دقيق (pairwise grid)**. أضفنا أيضاً معالجة أخطاء الشبكة (timeouts) وفلترة للعلم عبر regex. هذه الخُطّة أدت في النهاية لاستخراج العلم:

```

sun{wh4t_4_gr34t_pr0j3ct}

````

---

## وصف المشكلة
- الخدمة: `nc chal.sunshinectf.games 25201` (بروتوكول TCP بسيط يستقبل JSON ويعيد JSON يحتوي على `generation`, `average`, `scores`)
- واجهة الاختبار: ترسل JSON بصيغة `{ "samples": [[...],[...], ...] }` حيث كل عيّنة طولها 10 أرقام 0..1. الخادم يقيم الجيل ويعيد المتوسط.
- هدف المهاجم (أنت): إيجاد متجه جينات يحقق أو يتجاوز متوسط 95% خلال ≤100 تقييمات/أجيال أو أن تجذب الخادم لطباعة العلم.

المهمة عبارة عن مشكلة **black-box optimization** مع ميزات عشوائية واضحة في الاستجابة (أي التنفيذ ليس حتميًّا تمامًا)، لذا استخدمنا استراتيجيات تستغل العشوائية بخطة منظمة.

---

## الفكرة العامة للتقريب
1. نبدأ بعينة عشوائية `candidate` (طول 10). نكرّر لعدد مخصص من التقييمات (budget).
2. في كل تقييم نُولِّد جارٍ `neighbor` عبر تعديل عنصر واحد (أو عناصر قليلة) بإضافة Gaussian noise مع انحراف معياري `sigma` المتناقص تدريجيًا (annealing).
3. نقبل الجار إذا حسّن المتوسط أو بشكل عشوائي بنسب صغيرة للسماح للهروب من قِمم محلية.
4. نُجري عدّة جلسات (restarts) باستراتيجيات مختلفة للـrandom seed أو sigma0 لزيادة احتمالات إيجاد منطقة جيدة.
5. عند ملاحظة "قيمة جيدة" (مثلاً `best_avg >= 94.2`) نشغّل **تنقيح محلي دقيق**: ننشئ شبكة (grid) ثنائية الأبعاد على زوج من الجينات الحساسة (استُدل عليها عبر probing/sensitivity) ونقيّم كل نقطة لاختيار أفضل موضع دقيق.
6. نتعامل مع أخطاء الشبكة (timeouts) ونعيد محاولة/نهرب من الجلسة إن فشلت بدلاً من إسقاط كل عملية طويلة.

المنهجية هي مزيج من بحث محلي (hillclimbing)، استكشاف (restart + random jumps)، وتنقيح دقيق (pairwise grid) حيث تحتاج "لمسات" صغيرة للانتقال من ~94.6 إلى ≥95.

---

## مفاهيم عمليّة مهمّة
- **Sigma annealing**: نبدأ sigma كبيرًا (مثلاً 0.45) للسماح بطفرة واسعة ثم ننخفض تدريجيًا إلى sigma صغير (~0.02) للـfine-tuning.
- **Accept with small probability**: حتى لو لم يتحسن، نقبل الطفرة عشوائياً بنسخة صغيرة (مثلاً 4%) لتفادي الوقوع في قمة محليّة ثابتة.
- **Multi-restart**: تشغيل 40–100 جلسة مستقلة يزيد جداً فرص عبور العتبة بسبب الطبيعة العشوائية للسيرفر.
- **Pairwise probing**: نجرب تغيير جين واحد في نقاط متقطعة لملاحظة الحساسية (sensitivity). ثم نختار زوج جينات الأكثر حساسية ونبني شبكة (grid) دقيقة حولهما.
- **Timeout handling**: ضبط recv/send timeout (مثلاً 10s) والتعامل مع استثناءات الشبكة حتى لا يتعطّل السكربت بأكمله.
- **Flag detection**: فحص كل مخرَج نصّي عن نمط `sun{...}` واسترجاعه فوراً.

---

## ملفات/أوامر استخدمت
- `player.py` — السكربت الذي قدّمته المسابقة (يوفر وظائف لإرسال JSON واستقبال النتيجة).
- `multi_restart_resilient.py` — سكربت قمتُ بإنشائه/تعديله ليجري جلسات متكررة مع timeout handling وpairwise refine.

تشغيل نموذجي:

```bash
python3 multi_restart_resilient.py --host chal.sunshinectf.games --port 25201 --restarts 40 --budget 100 --sigma0 0.45 --sigma1 0.02 --recv_timeout 10
````

أوامر مفيدة أخرى (للبحث الموجّه):

```bash
# grid refine على جولتين جينات محددتين 1 و7
python3 player.py --host chal.sunshinectf.games --port 25201 --g0 1 --g1 7 --half 0.08 --points 8

# probing لتقييم حساسية جين
python3 player.py --probe --gene 1 --values "0.1,0.2,0.3,0.4,0.5"
```

---

## مثال مبسّط للوظائف الأساسية (مقتطفات كود)

### إرسال وقراءة JSON مع تحمّل الأخطاء

```python
def send_and_receive_json(sock, payload_bytes, timeout=10.0):
    try:
        sock.settimeout(timeout)
        if not payload_bytes.endswith(b"\n"):
            payload_bytes += b"\n"
        sock.sendall(payload_bytes)
    except Exception as e:
        return None, f"SEND_ERR:{e}"
    # قراءة للبافر ومحاولة تحميل JSON
    buf = b""
    end = time.time() + timeout
    while time.time() < end:
        try:
            chunk = sock.recv(4096)
        except socket.timeout:
            chunk = b""
        if chunk:
            buf += chunk
            try:
                parsed = json.loads(buf.decode(errors='ignore'))
                return parsed, buf.decode(errors='ignore')
            except:
                pass
        else:
            time.sleep(0.02)
    return None, buf.decode(errors='ignore')
```

### توليد جار عبر Gaussian mutation

```python
def neighbor(candidate, sigma):
    c = candidate[:]
    i = random.randrange(len(c))
    c[i] = max(0.0, min(1.0, c[i] + random.gauss(0, sigma)))
    return c
```

### pairwise refine (شبكة 2D حول زوج جينات)

```python
def pairwise_refine(sock, base_candidate, genes, remaining_evals, half_width=0.03, points=7):
    g0, g1 = genes
    grid0 = [clamp(base_candidate[g0] - half_width + i*(2*half_width)/(points-1), 0, 1) for i in range(points)]
    grid1 = [clamp(base_candidate[g1] - half_width + i*(2*half_width)/(points-1), 0, 1) for i in range(points)]
    best = (-1, None)
    used = 0
    for v0 in grid0:
        for v1 in grid1:
            if used >= remaining_evals: break
            cand = base_candidate[:]
            cand[g0] = v0; cand[g1] = v1
            parsed, raw = send_and_receive_json(sock, make_payload(cand))
            used += 1
            avg = parse_avg(parsed)
            if avg and avg > best[0]:
                best = (avg, cand[:])
    return best[0], best[1], used
```

---

## ماذا نجح ولماذا؟

* الجينات الواضحة/الحساسة (مثلاً الجين 1 و7 في إحدى الجلسات) سمحت لنا بعمل تنقيح محلي صغير جدًا (grid) فأحدث فرقًا كبيرًا في المتوسط.
* التبديل بين استكشاف واسع (sigma كبير، restarts متعددة) وتنقيح دقيق (sigma صغير + grid) أعطى أفضل نتيجتين: اكتشاف منطقة واعدة ثم ضبطها بدقّة صغيرة لعبور العتبة.
* التعامل مع أخطاء الشبكة وفرّ إعادة المحاولة، وحماية العمليات الطويلة، منع تعطّل الجلسات الناجحة بسبب timeout واحد.

---

## النّتائج

* وصلنا لدرجات قريبة ومتعدّدة من العتبة: جلسات عديدة أعطت متوسطات ≈ 94.2–94.9%.
* في محاولة متعددة restart (40 جلسة) تمكّنا من الوصول إلى العلم:

```
sun{wh4t_4_gr34t_pr0j3ct}
```

---

## تحسينات مستقبلية ممكنة

* **Parallelization**: تشغيل restarts متوازية عبر عمليات/ماكينات مختلفة لتسريع اكتشاف الحلول. يجب الحذر من قواعد الخدمة (rate limits).
* **استخدام خوارزميات تطورية أقوى**: CMA-ES أو population-based evolution قد ينجح أسرع في استكشاف الفضاء.
* **تخطيط ميزانية تقييم ذكي**: استخدام Bayesian optimization (مثلاً GP-based) لتوجيه التقييمات نحو مناطق مرجّحة للاختراق.

---

## خاتمة

هذه المسألة مثال عملي على كيفية المزج بين أساليب البحث العشوائي المحلي والتنقيح الموجَّه لحل مسائل تحسين سوداء الصندوقية (black-box). الكمّ الكبير من محاولات الـrestarts + تنقيح محلي دقيق هو غالبًا مفتاح النجاح في بيئات عشوائية مثل هذه.
Full Code : 
```
#!/usr/bin/env python3
"""
multi_restart_resilient.py

Robust multi-restart hillclimb with:
 - larger socket timeouts
 - graceful handling of network errors (TimeoutError, ConnectionReset, etc.)
 - automatic focused pairwise refinement (grid) when best_avg in a session exceeds a threshold

Usage:
  python3 multi_restart_resilient.py --host chal.sunshinectf.games --port 25201 --restarts 40
  python3 multi_restart_resilient.py --restarts 40 --sigma0 0.45 --recv_timeout 1

Tunable args:
  --restarts  number of independent sessions (default 40)
  --budget    evals per session (default 100)
  --target    target percent (default 95.0)
  --refine_threshold  trigger refine if session best >= this (default 94.2)
  --refine_genes  comma separated indices for pair refine (default "1,7")
  --recv_timeout  socket timeout seconds (default 10.0)
"""
import socket, json, time, argparse, random, re, itertools

POP_SIZE = 100
GENOME_LEN = 10

def send_and_receive_json(sock, payload_bytes, timeout=10.0):
    """Send payload and read until a JSON object is parsed or timeout seconds elapsed.
       Returns (parsed_obj_or_None, raw_text_or_errstr). Raises nothing; always returns tuple.
    """
    try:
        sock.settimeout(timeout)
        if not payload_bytes.endswith(b"\n"):
            payload_bytes = payload_bytes + b"\n"
        sock.sendall(payload_bytes)
    except Exception as e:
        return None, f"SEND_ERR:{repr(e)}"
    buf = b""
    end_time = time.time() + timeout
    sock.settimeout(0.5)
    while time.time() < end_time:
        try:
            ch = sock.recv(4096)
        except socket.timeout:
            ch = b""
        except Exception as e:
            return None, f"RECV_ERR:{repr(e)}"
        if ch:
            buf += ch
            try:
                s = buf.decode(errors="ignore").strip()
            except:
                s = ""
            if s:
                # Try to parse entire buffer
                try:
                    parsed = json.loads(s)
                    return parsed, s
                except:
                    # try finding JSON object in buffer
                    si = s.find('{'); ei = s.rfind('}')
                    if si!=-1 and ei!=-1 and ei>si:
                        try:
                            parsed = json.loads(s[si:ei+1])
                            return parsed, s
                        except:
                            pass
        else:
            time.sleep(0.02)
    try:
        return None, buf.decode(errors="ignore")
    except:
        return None, repr(buf)[:1000]

def avg_from_parsed(parsed):
    if isinstance(parsed, dict):
        if "average" in parsed:
            try:
                avg = float(parsed["average"])
                if avg <= 1.0:
                    avg *= 100.0
                return avg
            except:
                pass
        if "scores" in parsed and isinstance(parsed["scores"], list) and parsed["scores"]:
            try:
                avg = float(parsed["scores"][0])
                if avg <= 1.0:
                    avg *= 100.0
                return avg
            except:
                pass
    return None

def make_payload(candidate):
    return json.dumps({"samples":[candidate]*POP_SIZE}).encode()

def clamp01(x):
    return max(0.0, min(1.0, x))

def neighbor(candidate, sigma):
    c = candidate[:]
    i = random.randrange(len(c))
    c[i] = clamp01(c[i] + random.gauss(0, sigma))
    return c

def pairwise_refine(sock, base_candidate, genes, remaining_evals, half_width=0.03, points=9, timeout=10.0):
    """Do a small fine grid on two genes using up to remaining_evals.
       Returns (best_avg, best_candidate, flag_or_None, evals_used)
    """
    g0, g1 = genes
    def gen_grid(center, half, pts):
        if pts==1: return [center]
        step = (2*half)/(pts-1)
        return [clamp01(center - half + i*step) for i in range(pts)]
    grid0 = gen_grid(base_candidate[g0], half_width, points)
    grid1 = gen_grid(base_candidate[g1], half_width, points)
    best_avg = -1.0
    best_cand = base_candidate[:]
    evals = 0
    for v0, v1 in itertools.product(grid0, grid1):
        if evals >= remaining_evals:
            break
        cand = base_candidate[:]
        cand[g0] = v0
        cand[g1] = v1
        parsed, raw = send_and_receive_json(sock, make_payload(cand), timeout=timeout)
        evals += 1
        avg = None
        if parsed:
            avg = avg_from_parsed(parsed)
        # sometimes parsed==None and raw contains JSON later; try to parse raw
        if avg is None and isinstance(raw, str):
            m = re.search(r"sun\{[^}]+\}", raw)
            if m:
                return 100.0, cand, m.group(0), evals
        if avg is not None and avg > best_avg:
            best_avg = avg
            best_cand = cand[:]
        # check raw for flag
        if isinstance(raw, str):
            m = re.search(r"(sun\{[^}]+\})", raw)
            if m:
                return avg if avg is not None else 100.0, cand, m.group(1), evals
    return best_avg, best_cand, None, evals

def run_one_session(host, port, budget, target, sigma0, sigma1, refine_genes=(1,7), refine_threshold=94.2, recv_timeout=10.0, seed=None):
    """Return tuple: (session_success_bool_or_None, best_avg_seen, flag_or_None)
       session_success_bool True if flag found; False if no flag but session completed; None if session failed to init/connect.
    """
    if seed is not None:
        random.seed(seed)
    try:
        sock = socket.socket()
        sock.settimeout(recv_timeout)
        sock.connect((host, port))
    except Exception as e:
        return None, None, f"CONNECT_ERR:{e}"
    try:
        # banner
        try:
            banner = sock.recv(4096).decode(errors="ignore")
        except:
            banner = ""
        # init random candidate
        current = [random.random() for _ in range(GENOME_LEN)]
        parsed, raw = send_and_receive_json(sock, make_payload(current), timeout=recv_timeout)
        if parsed is None:
            return False, None, f"INIT_RECV_FAIL:{raw[:200]}"
        curr_avg = avg_from_parsed(parsed)
        if curr_avg is None:
            return False, None, "INIT_PARSE_FAIL"
        best = (curr_avg, current[:], raw)
        evals = 1
        # hillclimb loop
        while evals < budget:
            t = evals / max(1, budget-1)
            sigma = sigma0 * (1-t) + sigma1 * t
            cand = neighbor(current, sigma)
            parsed, raw = send_and_receive_json(sock, make_payload(cand), timeout=recv_timeout)
            if parsed is None:
                # network hiccup — abort session gracefully
                return False, best[0], None
            avg = avg_from_parsed(parsed)
            evals += 1
            if avg is None:
                continue
            if avg > curr_avg or random.random() < 0.04:
                current = cand
                curr_avg = avg
            if avg > best[0]:
                best = (avg, cand[:], raw)
            # immediate flag check
            raw_text = raw if isinstance(raw, str) else str(raw)
            m = re.search(r"(sun\{[^}]+\})", raw_text)
            if m:
                return True, avg, m.group(1)
            # if we are past threshold trigger focused refine using remaining evals
            if best[0] >= refine_threshold:
                remaining = budget - evals
                if remaining >= 6:  # need at least a few evals for refine
                    # do small fine grid centered on best candidate on refine_genes
                    best_avg_ref, best_cand_ref, flag, used = pairwise_refine(sock, best[1], refine_genes, remaining, half_width=0.03, points=7, timeout=recv_timeout)
                    evals += used
                    if flag:
                        return True, best_avg_ref, flag
                    if best_avg_ref and best_avg_ref > best[0]:
                        best = (best_avg_ref, best_cand_ref, "")
                # otherwise continue hillclimb
        # session ended normally
        return False, best[0], None
    except Exception as e:
        # any unrecoverable socket error — close and report failed session
        return False, None, f"SESSION_ERR:{e}"
    finally:
        try:
            sock.close()
        except:
            pass

def multi_run(host, port, restarts, budget, target, sigma0, sigma1, refine_genes, refine_threshold, recv_timeout, seed=None):
    best_overall = (-1.0, None)
    for i in range(restarts):
        s = None if seed is None else seed + i
        print(f"\n=== SESSION {i+1}/{restarts} seed={s} ===")
        ok, best_avg, flag = run_one_session(host, port, budget, target, sigma0, sigma1, refine_genes=tuple(refine_genes), refine_threshold=refine_threshold, recv_timeout=recv_timeout, seed=s)
        if ok is True and flag:
            print("\n=== FLAG FOUND ===\n", flag)
            return True
        if best_avg is not None:
            print(f"Session {i+1} best avg = {best_avg:.6f}%")
            if best_avg > best_overall[0]:
                best_overall = (best_avg, None)
        else:
            print("Session", i+1, "failed or returned no avg. info. flag/err:", flag)
    print("\nAll restarts finished. Best overall avg seen:", best_overall[0])
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="chal.sunshinectf.games")
    parser.add_argument("--port", type=int, default=25201)
    parser.add_argument("--restarts", type=int, default=40)
    parser.add_argument("--budget", type=int, default=100)
    parser.add_argument("--target", type=float, default=95.0)
    parser.add_argument("--sigma0", type=float, default=0.45)
    parser.add_argument("--sigma1", type=float, default=0.02)
    parser.add_argument("--refine_threshold", type=float, default=94.2)
    parser.add_argument("--refine_genes", default="1,7")
    parser.add_argument("--recv_timeout", type=float, default=10.0)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()
    genes = [int(x) for x in args.refine_genes.split(",") if x.strip()]
    multi_run(args.host, args.port, args.restarts, args.budget, args.target, args.sigma0, args.sigma1, genes, args.refine_threshold, args.recv_timeout, args.seed)

```

