def add_manual_homework():
    """Form to manually add a homework."""
    st.write("### Add New Homework")

    # Subject, title, due date input
    subject = st.text_input("Subject")
    title = st.text_input("Title")
    due_date = st.date_input("Due Date", datetime.now().date())
    # importance = st.slider("Importance (1-5)", 1, 5, 1)
    importance = st.selectbox("Importance", options=["High", "Normal", "Low"])
    if st.button("Add Homework"):
        # New homework entry with status 'Pending'
        new_homework = {
            'subject': subject,
            'title': title,
            'due_date': due_date.isoformat(),
            'importance': importance,
            'status': 'Pending'  # All homework starts as Pending
        }

        # Load existing homework data
        homework_data = load_json("homework.json")

        # Append the new homework and save back to the file
        homework_data.append(new_homework)
        save_json("homework.json", homework_data)

        st.success(f"Homework '{title}' added successfully!")


def display_homework():
    """Display all homework stored in homework.json, ensuring no duplicates are shown."""
    
    # Load the homework data from the JSON file
    homework = load_data("homework.json")

    # Make current_time timezone-aware (adjust timezone as needed)
    timezone = pytz.timezone('Africa/Casablanca')
    current_time = datetime.now(timezone)

    # Ensure every homework entry has a 'status' field
    for hw in homework:
        if 'status' not in hw:
            hw['status'] = 'Not Done'  # Default status is 'Not Done'

    # Remove duplicates: Create a unique set based on 'subject', 'title', and 'due_date'
    unique_homework = []
    seen_entries = set()  # To keep track of seen (subject, title, due_date) combinations

    for hw in homework:
        identifier = (hw['subject'], hw['title'], hw['due_date'])
        if identifier not in seen_entries:
            seen_entries.add(identifier)
            unique_homework.append(hw)

    if unique_homework:
        # Sort homework by due date and status ('Not Done' first, 'Done' last)
        def sort_key(hw):
            hw_due = datetime.fromisoformat(hw['due_date'])
            if hw_due.tzinfo is None:
                hw_due = timezone.localize(hw_due)
            return (hw['status'] == 'Done', hw_due)  # 'Done' status will be sorted last

        # Sort by status and due date
        unique_homework.sort(key=sort_key)

        st.write("### Upcoming Homework (Sorted by Date and Status)")

        for i, hw in enumerate(unique_homework):
            hw_due = datetime.fromisoformat(hw['due_date'])

            # Ensure both hw_due and current_time are timezone-aware
            if hw_due.tzinfo is None:
                hw_due = timezone.localize(hw_due)

            # Add a checkbox for homework status with unique keys using enumerate
            is_done = hw.get('status', 'Not Done') == 'Done'
            checkbox_label = f"{hw['subject']} - {hw['title']}"
            if st.checkbox(checkbox_label, value=is_done, key=f"{hw['title']}_{i}"):
                hw['status'] = 'Done'
            else:
                hw['status'] = 'Not Done'

            # Display details of the homework
            st.write(f"📅 Due: {hw_due.strftime('%Y-%m-%d')}")
            st.write(f"Importance: {hw['importance']}")
            st.write("---")

        # Save the updated homework status back to the JSON file
        save_data("homework.json", unique_homework)
    else:
        st.warning("No upcoming homework found.")
