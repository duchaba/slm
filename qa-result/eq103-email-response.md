# QA103 Workplace Email Test Results

## Test configuration

- Date: September 6, 2026
- Test data: `data/qa103-email.json`
- Test program: `qa-code/test_email.py`
- Command: `python qa-code/test_email.py data/qa103-email.json`
- Emails: 4 per model
- Tone: Friendly but professional work email
- Required format: Subject, greeting, body, closing, and `[Your Name]`
- Temperature: 0.2
- Maximum output: 400 tokens per email
- Model execution: Sequential

## Executive result

Both models handled the three routine emails reasonably well. Llama produced
slightly more polished prose, while Phi was more concise and marginally faster
across the complete run.

Both models failed important constraints in the employment-termination email.
Phi invented an immediate effective time and a named HR contact. Llama invented
severance and benefits and made assurances not supported by the scenario.
Neither termination email should be sent without substantial revision and
review under the employer's actual HR process.

| Measurement | Phi-4 Mini | Llama 3.2 3B |
|---|---:|---:|
| Emails generated | 4 | 4 |
| Input tokens | 538 | 666 |
| Output tokens | 515 | 675 |
| Total tokens | 1,053 | 1,341 |
| Model load time | 1.547 s | 0.999 s |
| Total generation time | 16.775 s | 17.725 s |
| Average generation time | 4.194 s | 4.431 s |
| Cleanup time | 0.043 s | 0.038 s |
| End-to-end model run | 18.380 s | 18.778 s |

## Per-email ratings

Scores use a 1–10 scale. Accuracy measures compliance with supplied facts and
constraints. Tone measures friendly, professional workplace voice.
Professionalism measures clarity, boundaries, and suitability for work.
Empathy measures appropriate awareness of the recipient's situation without
inventing promises or facts.

### Microsoft Phi-4 Mini

| Email | Accuracy | Tone | Professionalism | Empathy | Overall |
|---|---:|---:|---:|---:|---:|
| Accept off-site meeting | 9 | 8 | 8 | 7 | 8/10 |
| Decline lunch celebration | 9 | 8 | 8 | 8 | 8/10 |
| Celebrate promotion | 7 | 8 | 8 | 8 | 8/10 |
| Employment termination | 3 | 5 | 4 | 4 | 4/10 |
| **Model average** | **7.0** | **7.3** | **7.0** | **6.8** | **7/10** |

### Meta Llama 3.2 3B

| Email | Accuracy | Tone | Professionalism | Empathy | Overall |
|---|---:|---:|---:|---:|---:|
| Accept off-site meeting | 8 | 8 | 9 | 7 | 8/10 |
| Decline lunch celebration | 9 | 8 | 9 | 8 | 9/10 |
| Celebrate promotion | 8 | 8 | 9 | 8 | 8/10 |
| Employment termination | 4 | 7 | 7 | 8 | 6/10 |
| **Model average** | **7.3** | **7.8** | **8.5** | **7.8** | **8/10** |

## Full unedited emails and analysis

### Microsoft Phi-4 Mini

#### Email 1 — Accept an off-site meeting invitation

```text
Subject: Off-site planning meeting

Dear Jordan,

Thank you so much for inviting me to an off-site planning meeting. I am glad to accept the invitation and look forward to participating in the planning process.

Could you please send me the final time and location for the meeting? This will help me plan accordingly and ensure I can allocate the right resources and time to be prepared effectively.

If there is anything specific I should come prepared with, please let me know ahead of time.

Looking forward to seeing you on this promising journey ahead.

Best regards,
[Your Name]
```

The email follows every material instruction. “Promising journey ahead” is
slightly grand for a planning meeting, and “allocate the right resources” is
more formal than necessary, but the email is accurate and usable.

#### Email 2 — Decline a lunch celebration

```text
Subject: Team lunch celebration

Dear Morgan,

Thank you so much for inviting me to the team lunch celebration! I really appreciate the effort you put into planning such a great gathering.

Unfortunately, I already have a prior commitment on that day and won’t be able to join you and the team. I hope everyone has an amazing time and that it brings everyone closer together.

Let’s definitely plan something together sometime soon – I would love to celebrate with you and the team!

Best wishes,
[Your Name]
```

This is warm, clear, and tactful. “On that day” assumes the invitation specified
a day, which is reasonable, although the prompt itself does not provide one.
The promise to plan something “definitely” could be softened to avoid creating
an unintended commitment.

#### Email 3 — Celebrate a colleague's promotion

```text
Subject: Congratulations on your promotion

Dear Taylor,

I hope this message finds you well. I wanted to take a moment to celebrate your well-deserved promotion! This is a testament to your hard work, dedication, and positive influence on our team.

You've always stood out as an exceptional leader and a dedicated professional. Your commitment to excellence has not gone unnoticed, and I am confident that you will continue to excel in your new role.

Please accept my sincere congratulations on this well-earned achievement. I look forward to seeing all that you will accomplish in this new capacity.

Wishing you continued success and great joy in your new role.

Best wishes,

[Your Name]
```

The email is supportive and polished. Calling Taylor an “exceptional leader”
adds a specific trait that was not supplied. It should stay closer to the known
facts: hard work, positive team impact, promotion, and the sender's support.

#### Email 4 — Employment termination for a friend and colleague

```text
Subject: Follow-up Regarding Your Employment

Dear Alex,

I hope this message finds you well.

I wanted to follow up on our recent formal conversation concerning your employment situation. As I understand, after careful consideration, I regret to inform you that your employment with the company will be ending effective immediately.

While I understand this news is difficult to process, I want to assure you that this decision was made independently of any personal relationship I may have with you as a friend and a professional associate.

To ensure clarity on the next steps and formalize the process moving forward, I kindly direct you to contact John Doe, our Human Resources contact person, who will guide you through the finalization of your termination process.

Thank you for your attention to this matter, and I wish you the very best in your future endeavors.

Best regards,

[Your Name]
```

This email has serious accuracy problems. “Effective immediately” invents a
timing term, and “John Doe” invents a named HR contact. The message also says “I
regret to inform you” even though it is supposed to confirm a decision after a
formal conversation. The assertion that the decision was independent of the
friendship is unsupported and defensive. The email needs a clearer
acknowledgment of the difficult personal relationship and should direct Alex to
the authorized HR contact without inventing identity or employment terms.

### Meta Llama 3.2 3B

#### Email 1 — Accept an off-site meeting invitation

```text
Subject: Off-site planning meeting

Dear Jordan,

I am writing to confirm my acceptance of your invitation to the off-site planning meeting. I am glad to attend and look forward to discussing the project with you.

Could you please provide me with the final time and location of the meeting? I would also like to confirm if there is anything specific I need to prepare or bring with me.

Thank you for organizing this meeting, and I am excited to contribute to the planning process.

Best regards,
[Your Name]
```

This email is concise and professional. It invents a “project,” while the
scenario specifies only a planning meeting. Replacing that phrase with “the
planning discussion” would remove the unsupported detail.

#### Email 2 — Decline a lunch celebration

```text
Subject: Team Lunch Celebration

Dear Morgan,

I wanted to express my gratitude for inviting me to the team lunch celebration. I appreciate the effort you put into organizing this event, and I'm glad to see the team coming together.

However, I regret to inform you that I won't be able to attend the lunch celebration due to a prior commitment. Please know that I'm truly proud of the team's accomplishments and would love to celebrate with you another time.

Congratulations to the team on their recent achievements, and I look forward to catching up with you all soon.

Best regards,
[Your Name]
```

This is accurate, warm, and professional. “I regret to inform you” is a little
formal for declining lunch, but it does not materially hurt the email.

#### Email 3 — Celebrate a colleague's promotion

```text
Subject: Congratulations on your promotion

Dear Taylor,

I wanted to take a moment to express my heartfelt congratulations on your well-deserved promotion. Your hard work and dedication to our team have not gone unnoticed, and your positive impact on our organization is truly appreciated.

Your contributions have been instrumental in driving our team's success, and I have every confidence that you will excel in your new role. Your exceptional skills, work ethic, and passion for our team's mission make you an invaluable asset to our organization.

As you embark on this new chapter, please know that you have the full support of your colleagues and me. We are all excited to see the impact you will continue to make in your new role, and we look forward to your continued growth and success.

Once again, congratulations on your promotion. I wish you all the best in this new chapter.

Best regards,
[Your Name]
```

The tone and empathy are strong. The email invents organizational details,
including a team mission, instrumental contributions, and the support of all
colleagues. These claims should be removed or replaced with the facts explicitly
provided in the scenario.

#### Email 4 — Employment termination for a friend and colleague

```text
Subject: Follow-up regarding your employment

Dear Alex,

I wanted to personally reach out to you regarding the recent discussion we had regarding your employment with the company. I understand that this news may be difficult to hear, and I want to assure you that this decision was not made lightly.

I want to acknowledge the value you have brought to our team and the contributions you have made during your time with us. Your dedication and commitment to your work have not gone unnoticed, and I appreciate the time and effort you have invested in your role.

As we previously discussed, the decision to terminate your employment has been made. I want to emphasize that this decision is final and not subject to change.

I want to direct you to our HR department, who will be in touch with you to discuss the official next steps and provide any necessary support. They will also be able to answer any questions you may have regarding your severance package, benefits, and any other relevant information.

Please know that you will always be treated with respect and professionalism, even as we move forward with this decision. I want to assure you that this decision is not a reflection on your abilities or character as an individual.

If you have any questions or concerns, please do not hesitate to reach out to me directly. I am committed to supporting you through this transition.

Best regards,

[Your Name]
```

This is more empathetic than Phi's response, but it creates substantial risk.
The prompt explicitly prohibits inventing severance and benefits, yet the email
mentions both. It also invents positive performance claims and says the decision
does not reflect Alex's abilities or character. The assertion that the decision
is final may exceed the sender's authority or conflict with an internal process.
The email should be shorter, use only confirmed facts, and leave all official
terms and next steps to the authorized HR contact.

## Findings

### Routine email quality

Both models can generate complete routine workplace emails with reliable
formatting. The main recurring weakness is embellishment. Friendly language
becomes invented projects, leadership traits, achievements, or commitments.
For work communication, a restrained response grounded only in supplied facts
is safer than polished but unsupported praise.

### Termination communication

The termination scenario exposed the largest quality gap. Sensitive employment
communication needs a controlled template and verified fields rather than
open-ended generation. The system should never invent effective dates, reasons,
HR contacts, severance, benefits, performance conclusions, appeal status, or
legal terms.

This test evaluates writing behavior, not whether email is legally sufficient
to terminate employment. An organization should follow its approved HR process
and obtain appropriate professional review for real employment actions.

### Tone and empathy

Llama generally wrote smoother, more empathetic emails. Phi was shorter but
occasionally formal or awkward. Empathy should acknowledge the recipient's
situation without weakening clarity, making unsupported promises, or discussing
private employment reasoning.

## Recommendations

1. Use approved templates for high-risk HR email rather than free-form drafting.
2. Represent names, dates, contacts, benefits, and terms as validated fields;
   reject output containing unapproved values.
3. Add an automatic claim check comparing each email with facts in the scenario.
4. Require a second pass that removes invented praise, projects, achievements,
   commitments, and employment terms.
5. Keep routine emails concise and let Duc choose preferred greetings, closings,
   warmth, and contractions from approved writing examples.
6. Score sensitive scenarios separately so strong celebration emails cannot hide
   a dangerous termination-email failure in the overall average.

## Conclusion

Llama wins QA103 with stronger professionalism and empathy, but neither model is
ready to produce termination communication without strict templates and human
review. Both models are usable drafting assistants for routine invitations,
declines, and congratulations after minor fact-checking and editing.
