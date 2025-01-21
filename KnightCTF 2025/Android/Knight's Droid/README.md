name : 

Knight's Droid

Des : 

For ages, a cryptic mechanical guardian has slumbered beneath the Knight’s Citadel. Some say it holds powerful secrets once wielded by ancient code-wielding Knights. Many have tried to reactivate the droid and claim its hidden knowledge—yet none have returned victorious. Will you be the one to solve its riddles and awaken this legendary machine?


Author : 
NomanProdhan




open : JADX 

![image](https://github.com/user-attachments/assets/050c31e2-03d9-421a-9344-44e804d817c6)


Ok ,, we see Function " verifyFlag " open it 

```
public class SecretKeyVerifier {
    private static final String ENC_SEG_A = "wp5_GJECD";
    private static final String ENC_SEG_B = "P_u0q_c0p_";
    private static final String ENC_SEG_C = "GYPB{_ykjcn";
    private static final String ENC_SEG_D = "uKqN_Gj1cd7_zN01z_}";

    public static boolean verifyFlag(Context context, String userInput) {
        String fullPackageName = context.getPackageName();
        if (fullPackageName.length() < 20) {
            return false;
        }
        String firstTen = fullPackageName.substring(0, 10);
        int shift = computeShiftFromKey(firstTen);
        String encodedUserInput = droidMagic(userInput, shift);
        return "GYPB{_ykjcnwp5_GJECDP_u0q_c0p_uKqN_Gj1cd7_zN01z_}".equals(encodedUserInput);
    }

    private static int computeShiftFromKey(String key) {
        int sum = 0;
        for (char c : key.toCharArray()) {
            sum += c;
        }
        return sum % 26;
    }

    private static String droidMagic(String input, int droidTask) {
        int droidTask2 = ((droidTask % 26) + 26) % 26;
        StringBuilder sb = new StringBuilder();
        for (char c : input.toCharArray()) {
            if (Character.isUpperCase(c)) {
                int originalPos = c - 'A';
                int newPos = (originalPos + droidTask2) % 26;
                sb.append((char) (newPos + 65));
            } else if (Character.isLowerCase(c)) {
                int originalPos2 = c - 'a';
                int newPos2 = (originalPos2 + droidTask2) % 26;
                sb.append((char) (newPos2 + 97));
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }
}
```


we Found "GYPB{_ykjcnwp5_GJECDP_u0q_c0p_uKqN_Gj1cd7_zN01z_}"

its "caesar cipher"

Use Solve Script : 

```
def caesar_cipher_decrypt(ciphertext, shift):
    decrypted_text = []
    shift = ((shift % 26) + 26) % 26  # Normalize the shift value
    for char in ciphertext:
        if 'A' <= char <= 'Z':  # Uppercase letters
            original_pos = ord(char) - ord('A')
            new_pos = (original_pos - shift) % 26
            decrypted_text.append(chr(new_pos + ord('A')))
        elif 'a' <= char <= 'z':  # Lowercase letters
            original_pos = ord(char) - ord('a')
            new_pos = (original_pos - shift) % 26
            decrypted_text.append(chr(new_pos + ord('a')))
        else:  # Non-alphabetic characters remain unchanged
            decrypted_text.append(char)
    return ''.join(decrypted_text)

# The encrypted text and shift value
encrypted_text = "GYPB{_ykjcnwp5_GJECDP_u0q_c0p_uKqN_Gj1cd7_zN01z_}"
shift_value = 22

# Decrypt the text
decrypted_text = caesar_cipher_decrypt(encrypted_text, shift_value)
decrypted_text

```

Flag :

```
KCTF{_congrat5_KNIGHT_y0u_g0t_yOuR_Kn1gh7_dR01d_}
```
