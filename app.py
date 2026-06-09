import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💖"
)

st.title("💖 연애상담 챗봇")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 오류: {e}")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요 😊 연애 고민이 있다면 편하게 이야기해주세요."
        }
    ]

# 기존 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
user_input = st.chat_input("연애 고민을 입력하세요...")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    try:
        # 시스템 프롬프트
        system_prompt = """
        당신은 따뜻하고 공감 능력이 높은 연애상담 전문가입니다.

        규칙:
        - 상대방을 비난하지 마세요.
        - 현실적이고 균형 잡힌 조언을 제공하세요.
        - 사용자의 감정을 먼저 공감하세요.
        - 위험하거나 폭력적인 행동은 권장하지 마세요.
        - 답변은 한국어로 작성하세요.
        """

        # 대화 기록 구성
        conversation = system_prompt + "\n\n"

        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "상담사"
            conversation += f"{role}: {msg['content']}\n"

        # Gemini 호출
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=conversation
        )

        answer = response.text

    except Exception as e:
        answer = f"오류가 발생했습니다.\n\n{e}"

    # 응답 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)
