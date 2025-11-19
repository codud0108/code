import streamlit as st
import random # 퀴즈 생성을 위해 추가

# --- 모스 부호 데이터 ---
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
    # 한글 이중모음 (퀴즈의 단순성을 위해 일부만 사용)
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
    # 문장 부호 (변환기에서 사용)
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
}

# --- 모스 부호 역변환 사전 (한/영 분리) ---
REVERSE_MORSE_KOREAN_DICT = {}
REVERSE_MORSE_ENGLISH_DICT = {}
KOREAN_JAMO_CHARS = (
    'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
    'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ',
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
)

for char, code in MORSE_CODE_DICT.items():
    if char in KOREAN_JAMO_CHARS:
        if code in REVERSE_MORSE_KOREAN_DICT:
            REVERSE_MORSE_KOREAN_DICT[code] += f'/{char}'
        else:
            REVERSE_MORSE_KOREAN_DICT[code] = char
    else:
        if code in REVERSE_MORSE_ENGLISH_DICT:
             REVERSE_MORSE_ENGLISH_DICT[code] += f'/{char}'
        else:
            REVERSE_MORSE_ENGLISH_DICT[code] = char


# --- 한글 분해 함수 ---
CHOSEONG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSEONG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSEONG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
COMPLEX_JAMO_DICT = {
    'ㅘ': 'ㅗㅏ', 'ㅙ': 'ㅗㅐ', 'ㅝ': 'ㅜㅓ', 'ㅞ': 'ㅜㅔ',
    'ㄳ': 'ㄱㅅ', 'ㄵ': 'ㄴㅈ', 'ㄶ': 'ㄴㅎ', 'ㄺ': 'ㄹㄱ', 'ㄻ': 'ㄹㅁ', 'ㄼ': 'ㄹㅂ',
    'ㄽ': 'ㄹㅅ', 'ㄾ': 'ㄹㅌ', 'ㄿ': 'ㄹㅍ', 'ㅀ': 'ㄹㅎ', 'ㅄ': 'ㅂㅅ'
}
C_MAP = {c: i for i, c in enumerate(CHOSEONG_LIST)}
V_MAP = {v: i for i, v in enumerate(JUNGSEONG_LIST)}
F_MAP = {f: i for i, f in enumerate(JONGSEONG_LIST)}

def decompose_hangul(char):
    """ 한글 한 글자를 자음/모음으로 분해합니다. """
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

# --- 자모를 완성된 한글로 합치는 함수 (변환기 출력에서만 사용하지 않음) ---
def combine_hangul(jamo_sequence):
    """ 분해된 자모 문자열을 완성된 한글 글자로 조합합니다. """
    UNICODE_BASE = 0xAC00
    result = []
    temp_syllable = []

    for char in jamo_sequence:
        ch_idx = C_MAP.get(char)
        ju_idx = V_MAP.get(char)
        fo_idx = F_MAP.get(char)

        # 1. 비-자모 문자 처리
        if ch_idx is None and ju_idx is None and (fo_idx is None or fo_idx == 0):
            if temp_syllable:
                ch_jamo, ju_jamo, fo_jamo = temp_syllable + [''] * (3 - len(temp_syllable))
                if ju_jamo:
                    result.append(chr(UNICODE_BASE + (C_MAP[ch_jamo] * 21 * 28) + (V_MAP[ju_jamo] * 28) + F_MAP[fo_jamo]))
                else:
                    result.append(ch_jamo) 
                temp_syllable.clear()
            result.append(char)
            continue
        
        # 2. 초성 (Choseong)
        if ch_idx is not None:
            if not temp_syllable or len(temp_syllable) == 3:
                temp_syllable = [char]
            elif len(temp_syllable) == 1:
                result.append(temp_syllable.pop(0))
                temp_syllable.append(char)
            elif len(temp_syllable) == 2:
                ch_jamo, ju_jamo = temp_syllable
                result.append(chr(UNICODE_BASE + (C_MAP[ch_jamo] * 21 * 28) + (V_MAP[ju_jamo] * 28) + 0))
                temp_syllable = [char]
        
        # 3. 중성 (Jungseong)
        elif ju_idx is not None:
            if len(temp_syllable) == 1:
                temp_syllable.append(char)
            else:
                result.append(chr(UNICODE_BASE + (C_MAP['ㅇ'] * 21 * 28) + (ju_idx * 28) + 0))
                temp_syllable.clear()
        
        # 4. 종성 (Jongseong)
        elif fo_idx is not None and fo_idx != 0:
            if len(temp_syllable) == 2:
                temp_syllable.append(char)
            else:
                result.append(char)
                temp_syllable.clear()

    if temp_syllable:
        ch_jamo, ju_jamo, fo_jamo = temp_syllable + [''] * (3 - len(temp_syllable))
        if ju_jamo:
            result.append(chr(UNICODE_BASE + (C_MAP[ch_jamo] * 21 * 28) + (V_MAP[ju_jamo] * 28) + F_MAP[fo_jamo]))
        else:
            result.append(ch_jamo)

    return ''.join(result)


# --- 모스 부호 변환 함수 ---
def text_to_morse(text):
    """ 텍스트를 모스 부호로 변환합니다. """
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
    """ 모스 부호를 텍스트로 변환하는 헬퍼 함수. """
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
    """ 텍스트에 대해 카이사르 암호를 적용합니다. """
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

# --- 퀴즈 관련 데이터 및 함수 ---
# 퀴즈에서 사용할 문자 리스트 (변환기에 포함된 문자 중 문장 부호 등 일부 제외)
QUIZ_CHAR_LIST_ALL = list(MORSE_CODE_DICT.keys())
QUIZ_CHAR_LIST_KOREAN = [c for c in QUIZ_CHAR_LIST_ALL if 'ㄱ' <= c <= 'ㅣ' and c not in COMPLEX_JAMO_DICT.keys()] # 복합 자모는 제외
QUIZ_CHAR_LIST_ENGLISH = [c for c in QUIZ_CHAR_LIST_ALL if 'A' <= c <= 'Z' or '0' <= c <= '9']

def generate_quiz_question(mode="char"):
    """ 퀴즈 질문 (모스 부호)와 정답 (텍스트)를 생성합니다. """
    if mode == "char":
        # 글자 모드: 단일 문자 (한글 자모, 영문, 숫자)
        char = random.choice(QUIZ_CHAR_LIST_KOREAN + QUIZ_CHAR_LIST_ENGLISH)
        morse = MORSE_CODE_DICT[char].replace('-', '_')
        return morse, char
    
    elif mode == "word":
        # 단어 모드: 여러 문자 조합 (3-6글자 길이)
        is_korean = random.choice([True, False])
        if is_korean:
            char_pool = QUIZ_CHAR_LIST_KOREAN
            word_len = random.randint(3, 5)
        else:
            char_pool = QUIZ_CHAR_LIST_ENGLISH
            word_len = random.randint(3, 6)
            
        text_word = ''.join(random.choice(char_pool) for _ in range(word_len))
            
        morse_codes = []
        for char in text_word:
            morse_codes.append(MORSE_CODE_DICT[char].replace('-', '_'))
                
        # 모스 부호는 글자별로 한 칸 띄어서 표시
        morse_word = ' '.join(morse_codes) 
        return morse_word, text_word

def set_quiz_mode(mode):
    """ 퀴즈 모드를 설정하고 점수를 초기화합니다. """
    st.session_state.quiz_mode = mode
    st.session_state.quiz_score = 0
    st.session_state.quiz_total = 0
    st.session_state.feedback = ""
    st.session_state.user_answer_input = "" # 입력 초기화
    new_question()

def new_question():
    """ 새로운 퀴즈 문제를 생성하고 상태를 업데이트합니다. """
    morse, answer = generate_quiz_question(st.session_state.quiz_mode)
    st.session_state.morse_question = morse
    st.session_state.answer_text = answer
    st.session_state.feedback = ""
    st.session_state.user_answer_input = ""

def check_answer():
    """ 사용자 입력을 확인하고 피드백을 제공합니다. """
    user_input = st.session_state.user_answer_input.strip().upper()
    correct_answer = st.session_state.answer_text.upper()
    
    # 입력이 없으면 확인하지 않음
    if not user_input:
        return 

    st.session_state.quiz_total += 1
    
    if user_input == correct_answer:
        st.session_state.quiz_score += 1
        st.session_state.feedback = f"✅ 정답입니다! 다음 문제로 넘어갑니다."
    else:
        st.session_state.feedback = f"❌ 오답입니다. 정답은 '{correct_answer}'입니다."
    
    # 0.5초 대기 후 다음 문제 생성 (Streamlit에서는 sleep 사용 불가, 즉시 다음 문제 생성)
    new_question()

def morse_quiz_page():
    """ 모스 부호 퀴즈 페이지 UI를 구성합니다. """
    st.title("🎧 모스 부호 퀴즈")
    st.markdown("랜덤으로 생성된 모스 부호를 보고 해당하는 문자를 맞춰보세요.")
    
    # Session State 초기화
    if 'quiz_mode' not in st.session_state:
        st.session_state.quiz_mode = 'char'
    if 'morse_question' not in st.session_state:
        st.session_state.morse_question = '?'
        st.session_state.answer_text = '?'
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_total' not in st.session_state:
        st.session_state.quiz_total = 0
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ""
        
    # --- 모드 선택 버튼 ---
    st.subheader("모드 선택")
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        # 이미 선택된 모드이면 버튼 비활성화
        if st.session_state.quiz_mode == 'char':
            st.button("글자 맞추기 (Character Mode)", disabled=True)
        else:
            if st.button("글자 맞추기 (Character Mode)"):
                set_quiz_mode('char')
    with col_mode2:
        if st.session_state.quiz_mode == 'word':
            st.button("단어 맞추기 (Word Mode)", disabled=True)
        else:
            if st.button("단어 맞추기 (Word Mode)"):
                set_quiz_mode('word')
    
    # 초기 질문 생성
    if st.session_state.quiz_total == 0 and st.session_state.morse_question == '?':
        new_question()
            
    # --- 점수 및 현재 모드 표시 ---
    st.subheader(f"점수: {st.session_state.quiz_score} / {st.session_state.quiz_total}")
    st.markdown(f"현재 모드: **{'글자 맞추기' if st.session_state.quiz_mode == 'char' else '단어 맞추기'}**")

    # --- 문제 표시 ---
    st.markdown("---")
    st.subheader("문제:")
    st.markdown(f"**길이: {len(st.session_state.answer_text)} {'글자' if st.session_state.quiz_mode == 'char' else '단어'}**")
    st.code(st.session_state.morse_question, language='text')

    # --- 사용자 입력 및 피드백 ---
    input_label = "정답 입력 (한글 자모 또는 영문):"
    help_text = "정답을 입력하고 Enter를 누르거나, 입력창 밖을 클릭하세요."
    if st.session_state.quiz_mode == 'word':
        input_label = "정답 입력 (띄어쓰기 없는 연속된 한글 자모 또는 영문 단어):"
        
    # 'on_change'를 사용하여 입력이 완료되면 자동으로 정답 확인 및 다음 문제로 전환
    st.text_input(input_label, 
                  key="user_answer_input", 
                  on_change=check_answer, 
                  help=help_text)
    
    if st.session_state.feedback:
        if st.session_state.feedback.startswith("✅"):
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)

# --- Streamlit 앱 UI 구성 ---

def main():
    st.set_page_config(page_title="암호 변환기 & 퀴즈", layout="wide")
    st.sidebar.title("메뉴")
    page = st.sidebar.radio("기능 선택", ["앱 설명", "모스 부호 변환기", "카이사르 암호 변환기", "모스 부호 퀴즈"])

    if page == "앱 설명":
        st.title("💡 모스 부호 & 카이사르 암호 변환기")
        st.markdown("""
        환영합니다! 이 앱은 두 가지 고전적인 암호 방식을 체험하고 모스 부호 퀴즈를 즐길 수 있는 도구입니다.

        왼쪽 사이드바에서 원하는 기능을 선택하세요.
        - **변환기:** 텍스트를 모스 부호나 카이사르 암호로 변환하거나 해독합니다.
        - **퀴즈:** 무작위로 생성된 모스 부호를 보고 문자를 맞추는 게임입니다.
        """)

    elif page == "모스 부호 변환기":
        st.title("Morse 부호 변환기")
        st.markdown("""
        모스 부호(Morse Code)는 짧은 신호(점, `.` )와 긴 신호(선, `_` )를 조합하여 문자를 나타내는 통신 방식입니다. 
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
                text_out_jamo = _morse_to_text_helper(morse_in, REVERSE_MORSE_KOREAN_DICT)
                
                # [수정 반영] 한글 자모 분리 결과만 표시
                st.text_area("변환 결과 (한글 자모):", value=text_out_jamo, height=70, disabled=True)
                
                # 영문/숫자/기호 결과
                text_out_english = _morse_to_text_helper(morse_in, REVERSE_MORSE_ENGLISH_DICT)
                st.text_area("변환 결과 (영문/숫자/기호):", value=text_out_english, height=70, disabled=True)
            else:
                st.warning("변환할 모스 부호를 입력하세요.")

    elif page == "카이사르 암호 변환기":
        st.title("🏛️ 카이사르 암호 변환기")
        st.markdown("""
        카이사르 암호는 영문자를 일정한 거리(키 값)만큼 밀어서 바꿉니다.
        
        슬라이더로 키를 선택하세요: **양수**는 오른쪽(암호화), **음수**는 왼쪽(복호화)으로 이동시킵니다.
        """)
        st.info("카이사르 암호는 영문자(A-Z, a-z)만 변환합니다. 한글, 숫자, 기호는 변환되지 않고 그대로 유지됩니다.")

        # --- 키 값을 +- 25로 설정하고 단일 버튼으로 처리 ---
        shift_key = st.slider("키(Key) 선택 (음수: 왼쪽, 양수: 오른쪽):", min_value=-25, max_value=25, value=3)
        
        text_in_caesar = st.text_area("변환할 텍스트 입력:", key="caesar_text")
        
        if st.button("변환하기", key="btn_transform"):
            if text_in_caesar:
                transformed_text = caesar_cipher(text_in_caesar, shift_key)
                st.text_area(f"변환 결과 (Key: {shift_key}):", 
                             value=transformed_text, 
                             height=150, 
                             disabled=True, 
                             key="caesar_out")
            else:
                st.warning("변환할 텍스트를 입력하세요.")
                
    elif page == "모스 부호 퀴즈":
        morse_quiz_page()

if __name__ == "__main__":
    main()
