# Criterion 1 evidence: retrieved chunks (before)

Produced by `store.py::search` (top-k 5, corpus campus_life), the same call `run_eval.py::run_once` makes. Retrieval is deterministic, so one pass shows what all three runs retrieved.

## What do students say about wait times at Kestrel Commons during lunch?

Expects: `20 to 25 minutes` -> found verbatim in 2 of 5 retrieved chunks

- CONTAINS `dining_kestrel_commons_followup.txt` (distance 0.262): Re: Kestrel Commons  Adding to what people have said about Kestrel Commons. The wait figure of 20 to 25 minutes between 12:15 and 1:00 matches what I've seen. If you're trying to eat between classes, go before 11:45 and 
-          `dining_halden_hall_followup.txt` (distance 0.413): Re: Halden Hall  Adding to what people have said about Halden Hall. The wait figure of rarely more than 8 minutes matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different buil
-          `dining_the_ridgeway_cafe_followup.txt` (distance 0.425): Re: The Ridgeway Café  Adding to what people have said about The Ridgeway Café. The wait figure of 10 to 15 minutes at 12:30 matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a dif
-          `dining_north_kitchen_followup.txt` (distance 0.437): Re: North Kitchen  Adding to what people have said about North Kitchen. The wait figure of none matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.
- CONTAINS `dining_kestrel_commons.txt` (distance 0.446): Kestrel Commons  I'm a junior and I've done this twice now. Wait times: 20 to 25 minutes between 12:15 and 1:00, under 5 minutes before 11:45. The thing worth going for is the stir-fry station, made to order. The thing t

## How much does a wash cost in the Aldridge Hall laundry room?

Expects: `$1.75` -> found verbatim in 4 of 5 retrieved chunks

- CONTAINS `housing_aldridge_hall_laundry.txt` (distance 0.226): Laundry in Aldridge Hall  Machines take $1.75 wash, $1.50 dry, card only. There are eight washers and six dryers for the building, which is the wrong ratio and means the dryers back up on Sunday evenings.
-          `housing_old_brewhouse.txt` (distance 0.320): Laundry costs $1.50 wash, $1.50 dry, coin only, and the machines are old. On noise: sound carries strangely because of the original brick; a room two floors up can be louder than next door.
- CONTAINS `housing_innisfree_hall.txt` (distance 0.354): Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
- CONTAINS `housing_calder_annexe.txt` (distance 0.358): Laundry costs $2.00 wash, $1.75 dry, app-based. On noise: depends entirely on your cluster; there's no building-wide pattern.
- CONTAINS `housing_aldridge_hall.txt` (distance 0.360): Laundry costs $1.75 wash, $1.50 dry, card only. On noise: quiet floors on 3 and 4 are genuinely enforced.

## How many hours per week outside of class should I expect for CS 210?

Expects: `8 to 10 hours` -> found verbatim in 2 of 5 retrieved chunks

- CONTAINS `course_cs_210.txt` (distance 0.242): Expect 8 to 10 hours a week outside class.
-          `course_stat_150.txt` (distance 0.258): Expect 5 to 6 hours a week outside class.
- CONTAINS `course_cs_210_workload.txt` (distance 0.260): Workload for CS 210 Data Structures  People keep asking so: 8 to 10 hours a week outside class. That's real time, not optimistic time.
-          `course_econ_101.txt` (distance 0.273): Expect 4 hours a week outside class.
-          `course_stat_150_workload.txt` (distance 0.311): Workload for STAT 150 Applied Statistics  People keep asking so: 5 to 6 hours a week outside class. That's real time, not optimistic time.

## What is the campus printing quota per semester?

Expects: `$30` -> found verbatim in 1 of 5 retrieved chunks

- CONTAINS `admin_printing_quota.txt` (distance 0.337): On the printing quota  Every student gets $30 of printing per semester, which is roughly 600 black-and-white pages. It does not roll over. Colour costs eight times as much per page, which people discover after printing o
-          `money_textbooks.txt` (distance 0.556): The campus store price-matches, which is not advertised anywhere and you have to ask at the counter with the other listing on your phone.
-          `money_jobs.txt` (distance 0.561): Maximum is 20 hours a week during term. Most people find 10 to 12 is the point where it stops affecting coursework.
-          `admin_graduation_requirements.txt` (distance 0.591): On the graduation requirements  120 credit hours, a completed major, and the general education requirements. The one that trips people is the writing-intensive requirement: two courses, and they must be taken in differen
-          `money_textbooks.txt` (distance 0.610): Textbooks without paying full price  The library holds one copy of most required texts on two-hour reserve. For courses where the text is used constantly that isn't enough, but for the reading-light courses it's genuinel

## Until what time is the library open during term?

Expects: `2am` -> found verbatim in 5 of 5 retrieved chunks

- CONTAINS `study_library_hours.txt` (distance 0.248): Library hours and where to actually sit  Open until 2am during term, until 10pm during reading week, which is backwards and catches everyone out every single year.
- CONTAINS `housing_innisfree_hall_noise.txt` (distance 0.335): If you're someone who needs quiet to work, the library is open until 2am during term and that's what most people in this building end up doing.
- CONTAINS `housing_old_brewhouse_noise.txt` (distance 0.335): If you're someone who needs quiet to work, the library is open until 2am during term and that's what most people in this building end up doing.
- CONTAINS `housing_tamsin_court_noise.txt` (distance 0.335): If you're someone who needs quiet to work, the library is open until 2am during term and that's what most people in this building end up doing.
- CONTAINS `housing_morrow_house_noise.txt` (distance 0.335): If you're someone who needs quiet to work, the library is open until 2am during term and that's what most people in this building end up doing.

