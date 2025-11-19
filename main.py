import streamlit as st

# --- 모스 부호 데이터 ---
# (기존과 동일)
MORSE_CODE_DICT = {
    # 한글 자음
    'ㄱ': '.-..', 'ㄴ': '--.', 'ㄷ': '-..', 'ㄹ': '...-', 'ㅁ': '--', 'ㅂ': '.--', 
    'ㅅ': '--.-', 'ㅇ': '-.-', 'ㅈ': '.--.', 'ㅊ': '-.-.', 'ㅋ': '-..-', 'ㅌ': '--..', 
    'ㅍ': '.---', 'ㅎ': '....',
    # 한글 된소리
    'ㄲ': '.-..-.', 'ㄸ': '-....', 'ㅃ': '.--.--', 'ㅆ': '--.--', 'ㅉ': '.--..-.',
    # 한글 모음
    'ㅏ': '.', 'ㅑ': '..', 'ㅓ': '-', 'ㅕ': '...', 'ㅗ': '.-', 'ㅛ': '.-.', 
    'ㅜ': '..-', 'ㅠ': '..-.', 'ㅡ': '-.--', 'ㅣ': '.-.',
    # 한글 이중모음
    'ㅐ': '.-.-', 'ㅔ': '-...-', 'ㅚ': '.-..-', 'ㅟ': '..--', 'ㅢ': '-..-', 'ㅒ': '..--.', 'ㅖ': '...-',

    # 영문 알파벳
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    # 숫자
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    # 문장 부호 (일부)
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
}

# --- 모스 부호 역변환 사전 (한/영 분리) ---
REVERSE_MORSE_KOREAN_DICT = {}
REVERSE_MORSE_ENGLISH_DICT = {}

# 한글 자모 문자열 집합
KOREAN_JAMO_CHARS = (
    'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
    'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ',
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
)

for char, code in MORSE_CODE_DICT.items():
    if char in KOREAN_JAMO_CHARS:
        # 겹치는 한글 자모가 있는지 확인 (예: '.-.'는 'R'과 'ㅣ'인데, 'ㅣ'는 한글에 포함)
        if code in REVERSE_MORSE_KOREAN_DICT:
            REVERSE_MORSE_KOREAN_DICT[code] += f'/{char}'
        else:
            REVERSE_MORSE_KOREAN_DICT[code] = char
    else:
        # 영문/기호/숫자
        if code in REVERSE_MORSE_ENGLISH_DICT:
             REVERSE_MORSE_ENGLISH_DICT[code] += f'/{char}'
        else:
            REVERSE_MORSE_ENGLISH_DICT[code] = char


# --- 한글 분해/합성을 위한 데이터 ---
# (사용되지 않지만, 혹시 모를 재사용을 위해 함수와 데이터는 유지)
CHOSEONG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSEONG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSEONG_LIST = [
    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 
    'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]
COMPLEX_JAMO_DICT = {
    'ㅘ': 'ㅗㅏ', 'ㅙ': 'ㅗㅐ', 'ㅝ': 'ㅜㅓ', 'ㅞ': 'ㅜㅔ',
    'ㄳ': 'ㄱㅅ', 'ㄵ': 'ㄴㅈ', 'ㄶ': 'ㄴㅎ', 'ㄺ': 'ㄹㄱ', 'ㄻ': 'ㄹㅁ', 'ㄼ': 'ㄹㅂ',
    'ㄽ': 'ㄹㅅ', 'ㄾ': 'ㄹㅌ', 'ㄿ': 'ㄹㅍ', 'ㅀ': 'ㄹㅎ', 'ㅄ': 'ㅂㅅ'
}
C_MAP = {c: i for i, c in enumerate(CHOSEONG_LIST)}
V_MAP = {v: i for i, v in enumerate(JUNGSEONG_LIST)}
F_MAP = {f: i for i, f in enumerate(JONGSEONG_LIST)}


def decompose_hangul(char):
    """ 한글 한 글자를 자음/모음으로 분해합니다. (기존과 동일) """
    code = ord(char)
    if 0xAC00 <= code <= 0xD7A3:
        code -= 0xAC00
        jongseong_index = code % 28
        code //= 28
        jungseong_index = code % 21
        code //= 21
        choseong_index = code
        ch = CHOSEONG_LIST[choseong_index]
        ju = JUNGSEONG_LIST[jungseong_index]
        jo = JONGSEONG_LIST[jongseong_index]
        if ju in COMPLEX_JAMO_DICT: ju = COMPLEX_JAMO_DICT[ju]
        if jo in COMPLEX_JAMO_DICT: jo = COMPLEX_JAMO_DICT[jo]
        return ch + ju + jo
    elif 'ㄱ' <= char <= 'ㅣ':
        if char in COMPLEX_JAMO_DICT:
            return COMPLEX_JAMO_DICT[char]
        else:
            return char
    else:
        return char

# --- 자모를 완성된 한글로 합치는 함수 (출력에서는 제외됨) ---
def combine_hangul(jamo_sequence):
    """
    분해된 자모 문자열을 완성된 한글 글자로 조합합니다.
    """
    UNICODE_BASE = 0xAC00
    result = []
    temp_syllable = []  # [초성, 중성, 종성] (최대 3개)

    for char in jamo_sequence:
        ch_idx = C_MAP.get(char)
        ju_idx = V_MAP.get(char)
        fo_idx = F_MAP.get(char)

        # 1. 비-자모 문자 (공백, 영문, 기호 등)
        if ch_idx is None and ju_idx is None and (fo_idx is None or fo_idx == 0):
            # 버퍼에 남은 자모가 있으면 먼저 처리
            if temp_syllable:
                ch_jamo, ju_jamo, fo_jamo = temp_syllable + [''] * (3 - len(temp_syllable))
                if ju_jamo: # C-V-F 또는 C-V
                    result.append(chr(UNICODE_BASE + (C_MAP[ch_jamo] * 21 * 28) + (V_MAP[ju_jamo] * 28) + F_MAP[fo_jamo]))
                else: # C 또는 V만 남은 경우 (V는 'ㅇ'으로 시작)
                    result.append(ch_jamo) 
                temp_syllable.clear()
            result.append(char)
            continue
        
        # 2. 초성 (Choseong)
        if ch_idx is not None:
            if not temp_syllable or len(temp_syllable) == 3:
                # 버퍼 비었거나(새 시작) C-V-F 완료 상태: 새 초성으로 시작
                temp_syllable.append(char)
            elif len(temp_syllable) == 1:
                # C + C (글자 아님): 이전 C를 독립 문자 처리, 새 초성 시작
                result.append(temp_syllable.pop(0))
                temp_syllable.append(char)
            elif len(temp_syllable) == 2:
                # C-V + C (새 글자 시작): 이전 C-V를 완성(종성X), 새 초성 시작
                ch_jamo, ju_jamo = temp_syllable
                result.append(chr(UNICODE_BASE + (C_MAP[ch_jamo] * 21 * 28) + (V_MAP[ju_jamo] * 28) + 0))
                temp_syllable = [char]
        
        # 3. 중성 (Jungseong)
        elif ju_idx is not None:
            if len(temp_syllable) == 1:
                # C + V: 중성 추가
                temp_syllable.append(char)
            else:
                # V or V-V: 독립 글자 ('ㅇ' + V)
                result.append(chr(UNICODE_BASE + (C_MAP['ㅇ'] * 21 * 28) + (ju_idx * 28) + 0))
                temp_syllable.clear()
        
        # 4. 종성 (Jongseong)
        elif fo_idx is not None and fo_idx != 0:
            if len(temp_syllable) == 2:
                # C-V + F: 종성 추가 (C-V-F)
                temp_syllable.append(char)
            else:
                # F만 온 경우: 독립 문자로 처리
                result.append(char)
                temp_syllable.clear()


    # 최종 버퍼 정리
    if temp_syllable:
        ch_jamo, ju_jamo, fo_jamo = temp_syllable + [''] * (3 - len(temp_syllable))
        if ju_jamo:
            result.append(chr(UNICODE_BASE + (C_MAP[ch_jamo] * 21 * 28) + (V_MAP[ju_jamo] * 28) + F_MAP[fo_jamo]))
        else:
            result.append(ch_jamo)

    return ''.join(result)


# --- 모스 부호 변환 함수 ---
def text_to_morse(text):
    """ 텍스트를 모스 부호로 변환합니다. (기존과 동일) """
    morse_code = []
    decomposed_text = ""
    for char in text:
        decomposed_text += decompose_hangul(char)
    for char in decomposed_text:
        upper_char = char.upper()
        if upper_char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[upper_char].replace('-', '_'))
        elif upper_char == ' ':
            morse_code.append('/')
        else:
            morse_code.append('?')
    return ' '.join(morse_code)

def _morse_to_text_helper(morse_input, reverse_dict):
    """ 모스 부호를 텍스트로 변환하는 헬퍼 함수. (기존과 동일) """
    morse_input_normalized = morse_input.replace('_', '-')
    words = morse_input_normalized.split(' / ')
    decoded_text = []
    
    for word in words:
        letters = word.split(' ')
        decoded_word = ''
        for letter in letters:
            if letter in reverse_dict:
                decoded_word += reverse_dict[letter]
            elif letter == '':
                continue
            else:
                decoded_word += '?'
        decoded_text.append(decoded_word)
        
    return ' '.join(decoded_text)


# --- 카이사르 암호 변환 함수 ---
def caesar_cipher(text, shift):
    """
    텍스트에 대해 카이사르 암호를 적용합니다.
    shift: 음수 (왼쪽), 양수 (오른쪽)
    """
    result = ""
    for char in text:
        # 영문 대문자인 경우
        if 'A' <= char <= 'Z':
            new_ord = (ord(char) - ord('A') + shift) % 26 + ord('A')
            result += chr(new_ord)
        # 영문 소문자인 경우
        elif 'a' <= char <= 'z':
            new_ord = (ord(char) - ord('a') + shift) % 26 + ord('a')
            result += chr(new_ord)
        # 영문이 아닌 경우 (한글, 숫자, 기호 등) 그대로 유지
        else:
            result += char
            
    return result


# --- Streamlit 앱 UI 구성 ---

def main():
    st.sidebar.title("암호 변환기")
    page = st.sidebar.radio("메뉴 선택", ["main", "모스 부호", "카이사르 암호"])

    if page == "main":
        st.title("모스 부호 & 카이사르 암호 변환기")
        st.markdown("""
        환영합니다! 이 앱은 두 가지 고전적인 암호 방식을 체험할 수 있는 **모스 부호 & 카이사르 암호 변환기**입니다.

        왼쪽 사이드바에서 원하는 암호 방식을 선택하세요. 텍스트를 입력하면 즉시 모스 부호나 카이사르 암호로 변환해 주며, 반대로 암호문을 해독하여 원래 텍스트를 확인할 수도 있습니다.

        이 도구를 통해 암호학의 기본 원리를 재미있게 탐색해 보세요!
        """)

    elif page == "모스 부호":
        st.title("Morse 부호 변환기")
        st.markdown("""
        모스 부호(Morse Code)는 짧은 신호(점, `.` )와 긴 신호(선, `_` )를 조합하여 문자를 나타내는 통신 방식입니다. 
        가장 유명한 신호는 국제 조난 신호인 **'SOS' (`... ___ ...`)**입니다.
        """)
        
        st.info("텍스트를 모스 부호로 변환할 때, 완성된 한글('안녕')은 자음/모음('ㅇㅏㄴㄴㅕㅇ')으로 자동 분해되어 변환됩니다.")

        # 텍스트 -> 모스 부호
        st.subheader("텍스트 → 모스 부호")
        text_in = st.text_area("한글, 영문, 숫자 입력:", key="text_to_morse_in")
        if st.button("모스 부호로 변환", key="btn_text_to_morse"):
            if text_in:
                morse_out = text_to_morse(text_in)
                st.code(morse_out)
            else:
                st.warning("변환할 텍스트를 입력하세요.")

        # --- 모스 부호 -> 텍스트 UI ---
        st.subheader("모스 부호 → 텍스트")
        morse_in = st.text_area("모스 부호 입력 ( . / _ 사용 )", 
                                help="문자 구분: 띄어쓰기 1칸 | 단어 구분: ' / ' (띄어쓰기 후 / 띄어쓰기)",
                                key="morse_to_text_in")
        if st.button("텍스트로 변환", key="btn_morse_to_text"):
            if morse_in:
                # 1. 한글 자모 분리 결과 (예: ㅇㅏㄴㄴㅕㅇ)
                text_out_jamo = _morse_to_text_helper(morse_in, REVERSE_MORSE_KOREAN_DICT)
                
            
                st.text_area("변환 결과 (한글 자모):", value=text_out_jamo, height=70, disabled=True)
                
                # 영문/숫자/기호 결과
                text_out_english = _morse_to_text_helper(morse_in, REVERSE_MORSE_ENGLISH_DICT)
                st.text_area("변환 결과 (영문/숫자/기호):", value=text_out_english, height=70, disabled=True)
            else:
                st.warning("변환할 모스 부호를 입력하세요.")

    elif page == "카이사르 암호":
        st.title("카이사르 암호 변환기")
        st.markdown("""
        카이사르 암호(Caesar Cipher)는 가장 간단한 **치환 암호** 방식 중 하나입니다.
        알파벳의 각 문자를 **일정한 거리(키 값)**만큼 밀어서 다른 문자로 바꿉니다.
        
        슬라이더로 키를 선택하세요: **양수**는 문자를 오른쪽(암호화)으로, **음수**는 왼쪽(복호화)으로 이동시킵니다.
        """)
        st.info("카이사르 암호는 영문자(A-Z, a-z)만 변환합니다. 한글, 숫자, 기호는 변환되지 않고 그대로 유지됩니다.")

        # --- [수정] 키 값을 +- 25로 설정하고 단일 버튼으로 처리 ---
        shift_key = st.slider("키(Key) 선택 (음수: 왼쪽, 양수: 오른쪽):", min_value=-25, max_value=25, value=3)
        
        text_in_caesar = st.text_area("변환할 텍스트 입력:", key="caesar_text")
        
        if st.button("변환하기", key="btn_transform"):
            if text_in_caesar:
                transformed_text = caesar_cipher(text_in_caesar, shift_key)
                # 결과창에 키 값에 따른 설명 추가
                st.text_area(f"변환 결과 (Key: {shift_key}):", 
                             value=transformed_text, 
                             height=150, 
                             disabled=True, 
                             key="caesar_out")
            else:
                st.warning("변환할 텍스트를 입력하세요.")

if __name__ == "__main__":
    main()
