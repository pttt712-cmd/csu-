# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="홈케어 예약", layout="centered")
st.title("🏠 홈케어 서비스 ")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "services" not in st.session_state:
    st.session_state.services = {
        "청소": 11000,
        "장보기": 11000,
        "요리": 15000,
        "세탁": 10000,
        "아이돌봄": 12000,
        "노인/환자 케어": 10000
    }

# Step 1: 이름 + 주소
if st.session_state.step == 1:
    st.header("1️⃣ 이름 및 주소 입력")
    name = st.text_input("이름을 입력해주세요")
    address = st.text_input("주소를 입력해주세요")
    if st.button("다음"):
        if name and address:
            st.session_state.name = name
            st.session_state.address = address
            st.session_state.step = 2
        else:
            st.warning("이름과 주소를 모두 입력해주세요.")

# Step 2: 날짜 + 시간 선택
elif st.session_state.step == 2:
    st.header("2️⃣ 예약 날짜 및 시간 선택")
    today = datetime.today()
    date = st.date_input("예약 날짜 선택", min_value=today)
    time = st.time_input("예약 시간 선택", value=datetime.now().time())
    if st.button("다음"):
        st.session_state.date = date
        st.session_state.time = time
        st.session_state.step = 3

# Step 3: 서비스 선택 + 시간
elif st.session_state.step == 3:
    st.header("3️⃣ 서비스 및 시간 선택")
    service = st.selectbox("서비스 선택", list(st.session_state.services.keys()))
    hours = st.number_input("시간 입력 (시)", min_value=1, max_value=8, value=1)
    price_per_hour = st.session_state.services[service]
    total_price = price_per_hour * hours
    st.write(f"💰 총 가격: {total_price:,}₩ (1시간 = {price_per_hour:,}₩)")
    if st.button("다음"):
        st.session_state.service = service
        st.session_state.hours = hours
        st.session_state.total_price = total_price
        st.session_state.step = 4

# Step 4: 결제 방법 + 보험
elif st.session_state.step == 4:
    st.header("4️⃣ 결제 방법 및 보험 안내")
    payment_method = st.selectbox("결제 방법 선택", ["신용카드", "카카오페이", "현금"])
    st.write("✅ 서비스에는 기본 보험이 포함되어 있습니다.")
    if st.button("다음"):
        st.session_state.payment_method = payment_method
        st.session_state.step = 5

# Step 5: 직원 평가 + 사진 업로드
elif st.session_state.step == 5:
    st.header("5️⃣ 직원 평가 및 사진 업로드")
    rating = st.slider("직원 평가 점수", min_value=1, max_value=5, value=5)
    uploaded_file = st.file_uploader("사진 업로드 (선택)", type=["png", "jpg", "jpeg"])
    st.session_state.rating = rating
    st.session_state.uploaded_file = uploaded_file
    if st.button("다음"):
        # Giảm giá dựa trên đánh giá / ảnh
        discount = rating * 1000  # ví dụ: 1 điểm = 1000₩ giảm
        if uploaded_file:
            discount += 2000  # upload ảnh thêm giảm 2000₩
        st.session_state.discount = discount
        st.session_state.final_price = max(st.session_state.total_price - discount, 0)
        st.session_state.step = 6

# Step 6: 예약 확인 + 요약
elif st.session_state.step == 6:
    st.header("6️⃣ 예약 확인")
    st.write(f"이름: {st.session_state.name}")
    st.write(f"주소: {st.session_state.address}")
    st.write(f"예약 날짜: {st.session_state.date}")
    st.write(f"예약 시간: {st.session_state.time}")
    st.write(f"서비스: {st.session_state.service}")
    st.write(f"시간: {st.session_state.hours}시간")
    st.write(f"총 가격: {st.session_state.total_price:,}₩")
    st.write(f"할인: {st.session_state.discount:,}₩")
    st.write(f"최종 결제금액: {st.session_state.final_price:,}₩")
    st.write(f"결제 방법: {st.session_state.payment_method}")
    st.write(f"직원 평가: {st.session_state.rating}점")
    if st.session_state.uploaded_file:
        st.image(st.session_state.uploaded_file, caption="업로드한 사진", use_column_width=True)
    if st.button("예약 완료"):
        st.success("🎉 예약이 완료되었습니다!")
