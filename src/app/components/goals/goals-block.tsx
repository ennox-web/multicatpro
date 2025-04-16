"use client";

import { Basis, GoalInterface, GoalType } from '@/app/api/data/goal-data';
import styles from './goals-block.module.css';
import TagChipList from '../tag/tag-chip-list';
import { useState } from 'react';


export default function GoalsBlock({ goal }: { goal: GoalInterface }) {
    const [pinned, setPinned] = useState(goal.pinned);
    const [pinAnimation, setPinAnimation] = useState(false);

    var goalStyle = styles.goalsBlock;
    var goalTypeStyle = styles.default;
    var basis = ""
    var tagChipStyle = "";
    var goalButton = "";

    switch (goal.basis) {
        case Basis.DAILY:
            goalStyle = `${styles.goalsBlock} ${styles.dailyGoal}`
            goalTypeStyle = styles.dailyGoalType;
            basis = "day";
            tagChipStyle = "triadic";
            goalButton = styles.goalButtonDaily;
            break;
        case Basis.WEEKLY:
            goalStyle = `${styles.goalsBlock} ${styles.weeklyGoal}`
            goalTypeStyle = styles.weeklyGoalType;
            basis = "week";
            tagChipStyle = "primary";
            goalButton = styles.goalButtonWeekly;
            break;
        case Basis.MONTHLY:
            goalStyle = `${styles.goalsBlock} ${styles.monthlyGoal}`
            goalTypeStyle = styles.monthlyGoalType;
            basis = "month";
            tagChipStyle = "tertiary";
            goalButton = styles.goalButtonMonthly;
            break;
        case Basis.ANNUALLY:
            goalStyle = `${styles.goalsBlock} ${styles.annuallyGoal}`
            goalTypeStyle = styles.annuallyGoalType;
            basis = "year";
            tagChipStyle = "secondary";
            goalButton = styles.goalButtonAnnually;
            break;
    }

    function pinGoal(setAnimation: boolean) {
        setPinned(!pinned);
        setPinAnimation(setAnimation);
        // TODO: Update pinned status of goal
    }

    return (
        <div className={goalStyle}>
            <div className={styles.goalsHeader}>
                <div className={styles.test}>
                    {pinned &&
                        <button
                            className={`material-symbols-outlined ${pinAnimation ? styles.goalPin : ""} ${styles.pin}`}
                            onClick={() => { pinGoal(false) }}
                        >keep</button>
                    }
                    {!pinned &&
                        <button
                            className={`material-symbols-outlined ${styles.unpinned}`}
                            onClick={() => { pinGoal(true) }}
                        >radio_button_unchecked</button>
                    }
                </div>
                <div className={styles.mainHeader}>
                    <button className={`${styles.goalButton} ${goalButton}`}><h5>{goal.name}</h5></button>
                    <h6 className={goalTypeStyle}>{goal.basis.charAt(0) + goal.basis.slice(1).toLowerCase()}</h6>
                </div>
            </div>
            <div className={styles.goalDesc}>
                <div className={styles.goalMainDesc}>
                    <span className={`material-symbols-outlined ${styles.icon}`}>{goal.completed ? "check_box" : "check_box_outline_blank"}</span>
                    <span>
                        {goal.goalType === GoalType.PROGRESS ? "Make progress on" : "Complete"}
                        {!goal.projectType && " any"}
                        {goal.target === 1 ? ' a' : ` ${goal.target}`}
                        {goal.projectType ? ` ${goal.projectType}` : " "}
                        {goal.target > 1 ? " projects" : " project"}
                        {goal.basis !== Basis.DAILY && goal.targetFrequency && ` ${goal.targetFrequency}`}
                        {goal.frequency ? ` ${goal.frequency.toLowerCase()}${goal.targetFrequency > 1 ? "s" : ""}` : ""}
                        {` every ${basis}`}
                    </span>
                </div>
                <span>
                    {goal.tags && <TagChipList tags={goal.tags} rowIndex={0} style={tagChipStyle} />}
                </span>
            </div>
        </div>
    )
}