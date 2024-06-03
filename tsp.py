def get_conflicts(self, data, extended_checks=False, teacher_checks=False):
    """
    General fitness function to check for conflicts in scheduling.
    
    Parameters:
        data (dict): The data used for evaluation.
        extended_checks (bool): Whether to perform additional checks for extended fitness.
        teacher_checks (bool): Whether to include teacher-specific checks.
        
    Returns:
        int: Number of conflicts found.
    """
    conflicts = 0
    # Dictionary to count lectures per subject per week for each group
    countPairSC = {(class_name, subject): 0 for subject in data['subject'] for class_name in data['group']}
    # Dictionary to count classes per day for each group
    countPairGT = {(group_name, day): 0 for day in data['day'] for group_name in data['group']}
    # Dictionary to store the days each group has classes
    countPairG = {group_name: [] for group_name in data['group']}
    # Dictionary to store the classrooms a group uses in a day
    countPairGCD = {(group_name, day): [] for day in data['day'] for group_name in data['group']}
    # Dictionary to count classes per day for each teacher
    countPairTD = {(t, d): 0 for t in data.get('teacher', []) for d in data['day']}
    # Dictionary to map subjects to teachers
    subjectTeacher = {subject: teacher for subject, teacher in zip(data['subject'], data.get('teacher', []))}


    #Iterate over lectures to check for conflicts
    for i in range(len(self.representation)):
        for j in range(i + 1, len(self.representation)):
            lecture_i = self.representation[i]
            lecture_j = self.representation[j]

            # Check for overlapping lectures for the same group
            if (lecture_i.get_group() == lecture_j.get_group() and 
                lecture_i.get_timeslot() == lecture_j.get_timeslot() and 
                lecture_i.get_day() == lecture_j.get_day()):
                conflicts += 1

            # Checks if the same classroom is assigned to two lectures at the same time on the same day.
            if (lecture_i.get_classroom() == lecture_j.get_classroom() and 
                lecture_i.get_timeslot() == lecture_j.get_timeslot() and 
                lecture_i.get_day() == lecture_j.get_day()):
                conflicts += 1

            # Checks if the same group has the same subject more than once on the same day.
            if (lecture_i.get_group() == lecture_j.get_group() and 
                lecture_i.get_day() == lecture_j.get_day() and 
                lecture_i.get_subject() == lecture_j.get_subject()):
                conflicts += 1

            if teacher_checks:
                # Check if a professor is teaching two lectures simultaneously
                if (lecture_i.get_teacher() == lecture_j.get_teacher() and 
                    lecture_i.get_timeslot() == lecture_j.get_timeslot() and 
                    lecture_i.get_day() == lecture_j.get_day()):
                    conflicts += 1

        # Count lectures per subject per week for each group
        group_subject = (lecture_i.get_group(), lecture_i.get_subject())
        if group_subject in countPairSC:
            countPairSC[group_subject] += 1

        # Count classes per day for each group
        group_day = (lecture_i.get_group(), lecture_i.get_day())
        if group_day in countPairGT:
            countPairGT[group_day] += 1

        # Days each group has classes
        if lecture_i.get_group() in countPairG:
            if lecture_i.get_day() not in countPairG[lecture_i.get_group()]:
                countPairG[lecture_i.get_group()].append(lecture_i.get_day())

        # Classrooms a group uses in a day
        if group_day in countPairGCD:
            if lecture_i.get_classroom() not in countPairGCD[group_day]:
                countPairGCD[group_day].append(lecture_i.get_classroom())

        if teacher_checks:
            # Count classes per day for each teacher
            teacher_day = (lecture_i.get_teacher(), lecture_i.get_day())
            if teacher_day in countPairTD:
                countPairTD[teacher_day] += 1

            # Check if professor is teaching designated subjects
            if lecture_i.get_subject() in subjectTeacher and subjectTeacher[lecture_i.get_subject()] != lecture_i.get_teacher():
                conflicts += 1

    # Check for incorrect number of lectures per subject per week
    conflicts += sum(1 for count in countPairSC.values() if count != data['classesPerSubject'])

    if extended_checks:
        # Check if each group has more than 3 classes per day
        conflicts += sum(1 for count in countPairGT.values() if count > 3)

        # Check if a group does not have at least one free day
        conflicts += sum(1 for days in countPairG.values() if len(days) > len(data['day']) - 1)

        # Adds conflicts for groups that change classrooms on the same day.
        conflicts += sum(1 for classrooms in countPairGCD.values() if len(classrooms) > 1)

    if teacher_checks:
        # Check if professors have more than 3 classes per day
        conflicts += sum(1 for count in countPairTD.values() if count > 3)

    return conflicts


def get_fitness1(self, data):
    """
    This is the initial fitness function, the most straightforward one, where conflicts are scrutinized in the following scenarios:
        - A classroom being concurrently occupied by two distinct lectures.
        - Overlapping lectures for a group, attending two separate classes simultaneously.
        - Duplicate scheduling of the same lecture within a single day for a group.
        - Incorrect count of lectures per subject per week for a group, either exceeding or falling short of the required number.
    
    Parameters:
        data (dict): The dataset used for evaluation.
        
    Returns:
        int: Count of identified conflicts.
    """
    return get_conflicts(self, data, extended_checks=False, teacher_checks=False)


def get_fitness2(self, data):
    """
    Fitness function to check for additional scheduling conflicts:
        - Timetables without at least one free day.
        - Classroom changes within a single day.
        - Schedules exceeding the maximum number of classes per day.
    """
    return get_conflicts(self, data, extended_checks=True, teacher_checks=False)


def get_fitness3(self, data):
    """
    Fitness function to check for complex scheduling conflicts, including teacher-specific constraints:
        - Each teacher is limited to a maximum of three classes per day.
        - A professor cannot simultaneously teach two lectures.
        - A professor is associated with a specific subject, representing his/her/their area of expertise.
          Consequently, whenever a professor is assigned to teach other lectures, a conflict should be considered.
    """
    return get_conflicts(self, data, extended_checks=True, teacher_checks=True)