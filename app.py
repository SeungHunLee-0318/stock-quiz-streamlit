import streamlit as st
import pandas as pd
import time

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="주식 테마 이해도 퀴즈",
    page_icon="📈",
    layout="centered"
)

STUDENT_ID = "2024404001"
STUDENT_NAME = "이승훈"

# =========================
# 캐싱 함수
# =========================
@st.cache_data
def load_quiz_data():
    """
    퀴즈 데이터를 CSV 파일에서 불러오는 함수입니다.
    주식 테마 퀴즈 문항은 앱 실행 중 반복해서 사용되므로,
    매번 CSV 파일을 다시 읽지 않도록 Streamlit 캐싱을 적용했습니다.
    """
    time.sleep(1.5)  # 데모 영상에서 캐싱 효과를 보여주기 위한 의도적 지연
    return pd.read_csv("data/quiz_data.csv")


@st.cache_data
def calculate_result(total_score, total_questions):
    """
    정답 개수에 따라 주식 테마 이해도 결과를 계산하는 함수입니다.
    같은 점수에 대해서는 같은 결과가 나오므로 캐싱을 적용했습니다.
    """
    time.sleep(0.5)

    ratio = total_score / total_questions

    if ratio >= 0.8:
        return {
            "type": "테마 분석 고수형",
            "message": "기업의 주력 제품, 기술 키워드, 관련 테마를 비교적 정확히 이해하고 있습니다.",
            "recommendation": "추천 방향: 기업 공시, IR 자료, 산업 리포트를 함께 보며 테마의 실체를 검증해보세요."
        }
    elif ratio >= 0.5:
        return {
            "type": "테마 관심 성장형",
            "message": "주식 테마와 기업 정보를 어느 정도 알고 있지만, 세부 기술이나 제품 구분은 더 학습할 필요가 있습니다.",
            "recommendation": "추천 방향: 뉴스 제목만 보기보다 기업의 실제 사업 내용과 매출 구조를 함께 확인해보세요."
        }
    else:
        return {
            "type": "기초 탐색형",
            "message": "아직 주식 테마와 기업 기술 용어가 낯설 수 있습니다. 기초 개념부터 차근차근 정리하는 단계입니다.",
            "recommendation": "추천 방향: 관심 기업의 홈페이지, 사업보고서, 핵심 제품 설명을 먼저 읽어보세요."
        }


# =========================
# 세션 상태 초기화
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "submitted" not in st.session_state:
    st.session_state.submitted = False


# =========================
# 첫 화면: 학번/이름 표시
# =========================
st.title("📈 주식 테마 이해도 퀴즈 앱")

st.info(f"""
제출자 정보  
- 학번: {STUDENT_ID}  
- 이름: {STUDENT_NAME}
""")

st.write("""
이 앱은 주식 시장에서 자주 등장하는 기업, 테마, 기술 키워드를 퀴즈로 확인하는 웹 애플리케이션입니다.  
로그인 후 퀴즈를 풀면 정답 개수에 따라 사용자의 주식 테마 이해도를 확인할 수 있습니다.
""")

st.warning("""
본 앱은 학습용 퀴즈 앱이며, 특정 종목의 매수·매도 추천을 목적으로 하지 않습니다.
""")


# =========================
# 로그인 기능
# =========================
st.divider()
st.subheader("🔐 로그인")

USER_DB = {
    "student": "1234",
    "stock": "2024",
    "guest": "0000"
}

if not st.session_state.logged_in:
    user_id = st.text_input("아이디를 입력하세요")
    password = st.text_input("비밀번호를 입력하세요", type="password")

    login_btn = st.button("로그인")

    if login_btn:
        if user_id in USER_DB and USER_DB[user_id] == password:
            st.session_state.logged_in = True
            st.session_state.username = user_id
            st.success(f"{user_id}님, 로그인에 성공했습니다.")
            st.rerun()
        else:
            st.error("로그인 실패: 아이디 또는 비밀번호가 올바르지 않습니다.")

    with st.expander("테스트용 로그인 정보 보기"):
        st.write("아이디: `student` / 비밀번호: `1234`")
        st.write("아이디: `stock` / 비밀번호: `2024`")
        st.write("아이디: `guest` / 비밀번호: `0000`")

else:
    st.success(f"현재 로그인 상태: {st.session_state.username}")
    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.submitted = False
        st.rerun()


# =========================
# 퀴즈 기능
# =========================
if st.session_state.logged_in:
    st.divider()
    st.subheader("🧠 주식 테마 퀴즈")

    st.caption("각 문항을 읽고 정답이라고 생각하는 선택지를 고르세요.")

    with st.spinner("퀴즈 데이터를 불러오는 중입니다..."):
        quiz_df = load_quiz_data()

    st.success("퀴즈 데이터 로딩 완료! 같은 데이터를 다시 불러올 때는 캐싱 덕분에 더 빠르게 표시됩니다.")

    score = 0
    answers = {}

    with st.form("quiz_form"):
        for idx, row in quiz_df.iterrows():
            st.markdown(f"**Q{idx + 1}. {row['question']}**")

            selected = st.radio(
                label="답변 선택",
                options=[
                    row["option_1"],
                    row["option_2"],
                    row["option_3"],
                    row["option_4"]
                ],
                key=f"question_{idx}",
                label_visibility="collapsed"
            )

            correct_answer = row["answer"]

            if selected == correct_answer:
                score += 1

            answers[row["question"]] = {
                "selected": selected,
                "correct": correct_answer
            }

            st.write("")

        submitted = st.form_submit_button("결과 확인하기")

    if submitted:
        st.session_state.submitted = True

        result = calculate_result(score, len(quiz_df))

        st.divider()
        st.subheader("📊 퀴즈 결과")

        st.metric(label="정답 수", value=f"{score} / {len(quiz_df)}")
        st.markdown(f"### 당신의 유형: {result['type']}")
        st.write(result["message"])
        st.info(result["recommendation"])

        with st.expander("문항별 정답 확인"):
            for q, info in answers.items():
                if info["selected"] == info["correct"]:
                    st.success(f"✅ {q}\n\n내 답: {info['selected']} / 정답: {info['correct']}")
                else:
                    st.error(f"❌ {q}\n\n내 답: {info['selected']} / 정답: {info['correct']}")

        st.balloons()

else:
    st.warning("퀴즈를 풀려면 먼저 로그인해야 합니다.")
