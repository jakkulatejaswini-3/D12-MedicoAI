import streamlit as st

def main():
    # -----------------------------
    # Emergency Tips Database
    # -----------------------------
    emergency_tips = {
        "Heart Attack": """
        🚑 Actions if someone has a suspected heart attack:
        - Call emergency services immediately.
        - Keep the person calm and seated.
        - Loosen tight clothing.
        - If conscious and not allergic, give aspirin.
        - Begin CPR if unconscious and no pulse.
        """,

        "Stroke": """
        🚑 Actions if someone has a suspected stroke:
        - Call emergency services immediately.
        - Check for FAST signs: Face drooping, Arm weakness, Speech difficulty, Time to call emergency.
        - Do NOT give food or drink.
        """,

        "Severe Bleeding": """
        🚑 Actions for severe bleeding:
        - Apply firm pressure with a clean cloth or bandage.
        - Elevate the injured limb if possible.
        - Do NOT remove objects stuck in the wound.
        - Call emergency services if bleeding does not stop.
        """,

        "Choking": """
        🚑 Actions if someone is choking:
        - Encourage the person to cough forcefully.
        - Perform abdominal thrusts (Heimlich maneuver) if airway is blocked.
        - For infants: give back blows and chest thrusts.
        - Call emergency services if airway remains blocked.
        """,

        "Burns": """
        🚑 Actions for burns:
        - Remove the person from the source of the burn.
        - Cool the burn under running water for at least 10 minutes.
        - Do NOT apply ice, butter, or ointments.
        - Cover with a clean, non-fluffy cloth.
        - Seek medical help for severe burns.
        """,

        "Poisoning/Overdose": """
        🚑 Actions in case of poisoning or overdose:
        - Call emergency services immediately.
        - Do NOT induce vomiting unless instructed by a medical professional.
        - Keep drug/poison packaging for reference.
        - If unconscious, place the person in recovery position.
        """,

        "Allergic Reaction (Anaphylaxis)": """
        🚑 Actions during a severe allergic reaction:
        - Use an epinephrine auto-injector (EpiPen) if available.
        - Call emergency services immediately.
        - Keep airway open, loosen tight clothing.
        - Begin CPR if unconscious and needed.
        """,

        "Seizure": """
        🚑 Actions during a seizure:
        - Keep the person safe and remove harmful objects.
        - Place them on their side (recovery position).
        - Do NOT restrain or put anything in their mouth.
        - Time the seizure; call emergency services if it lasts more than 5 minutes.
        """,

        "General Emergency": """
        🚑 General emergency actions:
        - Stay calm.
        - Call your local emergency number immediately.
        - Provide first aid only if trained.
        - Keep the patient comfortable until help arrives.
        """
    }

    # -----------------------------
    # Streamlit UI
    # -----------------------------
    st.title("🚨 Emergency First Aid Tips")
    st.write("This tool provides quick first-aid instructions for common medical emergencies.")
    st.write("**Note:** This is not a replacement for professional medical care. Always call emergency services immediately.")

    # Dropdown menu for emergency situations
    choice = st.selectbox("Select emergency situation:", list(emergency_tips.keys()))

    # Display tips
    st.subheader(f"Emergency: {choice}")
    st.info(emergency_tips[choice])


if __name__ == "__main__":
    main()