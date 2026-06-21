import streamlit as st
import tempfile
import os
from core.transcriber import transcribe_audio
from core.analyzer import analyze_speech

st.set_page_config(page_title="English Buddy", page_icon="🎙️", layout="centered")

st.title("🎙️ English Buddy")
st.caption("Speak. Get feedback. Improve.")
st.divider()

# --- Session state ---
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None

# --- Record Section ---
if not st.session_state.transcript:
    st.subheader("🎤 Record Your Speech")
    st.write("Speak for **30–60 seconds** on any topic. We'll analyze your grammar, pace, and clarity.")

    audio = st.audio_input("Click the mic below to start recording")

    if audio is not None:
        with st.spinner("Transcribing your speech..."):
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio.getvalue())
                tmp_path = tmp.name

            transcript = transcribe_audio(tmp_path)
            os.unlink(tmp_path)

        if not transcript:
            st.error("Could not transcribe audio. Please try again.")
        else:
            # Estimate duration from file size (rough: 16kHz 16-bit mono = 32000 bytes/sec)
            duration_estimate = max(10, len(audio.getvalue()) / 32000)

            with st.spinner("Getting AI feedback..."):
                analysis = analyze_speech(transcript, duration_seconds=duration_estimate)

            st.session_state.transcript = transcript
            st.session_state.analysis = analysis
            st.rerun()

# --- Results ---
if st.session_state.transcript and st.session_state.analysis:
    transcript = st.session_state.transcript
    analysis = st.session_state.analysis

    st.subheader("📊 Your Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Clarity Score", f"{analysis['clarity_score']} / 10")
    col2.metric("Speaking Pace", f"{analysis['wpm']} WPM")
    col3.metric("Filler Words", analysis['filler_words']['total'])

    st.caption(f"_{analysis['pace_feedback']}_")
    st.divider()

    st.subheader("📝 What You Said")
    st.info(transcript)

    st.subheader("🔁 Filler Words Breakdown")
    breakdown = analysis["filler_words"]["breakdown"]
    if not breakdown:
        st.success("✅ No filler words detected!")
    else:
        cols = st.columns(min(len(breakdown), 5))
        for i, (word, count) in enumerate(breakdown.items()):
            cols[i % 5].metric(f'"{word}"', f"× {count}")

    st.subheader("✏️ Grammar Corrections")
    issues = analysis.get("grammar_issues", [])
    if not issues:
        st.success("✅ No major grammar issues found!")
    else:
        for issue in issues:
            with st.expander(f"✗ {issue['original']}"):
                st.markdown(f"**✓ Correction:** {issue['correction']}")
                st.caption(issue['explanation'])

    st.subheader("⭐ Improved Version")
    st.success(analysis["improved_version"])

    st.subheader("💡 Tips for You")
    for tip in analysis.get("confidence_tips", []):
        st.markdown(f"- {tip}")

    st.divider()
    if st.button("🔄 Try Again", use_container_width=True):
        st.session_state.transcript = None
        st.session_state.analysis = None
        st.rerun()
