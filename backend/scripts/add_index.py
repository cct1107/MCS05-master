import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract_data.extract_from_pdf import extract_text_from_pdf
from extract_data.extract_from_url import extract_article_text
from extract_data.extract_from_csv import extract_food_gi
from extract_data.chunker import split_into_chunks_1, split_into_chunks_2, split_into_chunks_3, split_into_chunks_4, split_into_chunks_6, split_into_chunks_h3
from process_dataset.build_dataset import add_chunks_to_index, add_chunks_to_bm25


index_filename = "faiss_index.index"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

index_path = os.path.join(BASE_DIR, "faiss_index.index")
doc_store_path = os.path.join(BASE_DIR, "doc_store.json")
bm25_path = os.path.join(BASE_DIR, "bm25.pkl")

if __name__ == "__main__":
    chunks = []

    # # PDF
    pdf_files = [
        # "backend/documents/1452-1-3002-1-10-20180628.pdf",

    ]

    for pdf_file in pdf_files:
        text = extract_text_from_pdf(pdf_file)
        chunks += split_into_chunks_6(text)
        print(f"✅ Processed {pdf_file}")

    # Web articles
    url_list = ["https://www.webmd.com/diabetes/stop-prediabetes-progression",
    "https://www.webmd.com/diabetes/diabetes-causes",
    "https://www.webmd.com/diabetes/ss/slideshow-prediabetes-diet",    
    "https://www.webmd.com/diet/glycemic-index-diet",
    "https://www.webmd.com/diabetes/ss/slideshow-snacks-blood-sugar",

        
        
        "https://www.webmd.com/diabetes/how-sugar-affects-diabetes",
        "https://www.webmd.com/diabetes/cm/t2d-reversed-remission",
        "https://blogs.webmd.com/diabetes/20240207/5-blood-sugar-friendly-swaps-for-valentines-day",
        "https://www.webmd.com/diet/glycemic-index-diet",
        "https://www.webmd.com/diabetes/glucose-diabetes",
        "https://www.webmd.com/diabetes/causes-blood-sugar-spikes",
        "https://www.webmd.com/diabetes/features/blood-sugar-level-older-adults",
        "https://www.webmd.com/diet/news/20240911/ultra-processed-doesnt-always-mean-bad-how-to-tell",
    
        "https://gleneagles.com.my/health-digest/prediabetes",
        "https://codeblue.galencentre.org/2025/05/one-in-10-people-with-prediabetes-are-likely-to-develop-type-2-diabetes-in-a-year/"
        ]
    for url in url_list:
        text = extract_article_text(url)
        chunks += split_into_chunks_h3(text)
        print(f"✅ Processed {url}")


    # CSV
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # csv_path = os.path.join(base_dir, "documents", "GI_Table.csv")
    # chunks += extract_food_gi(csv_path)

    # # Additional manual chunks
    chunks += [

]




    add_chunks_to_index(chunks, index_path, doc_store_path)
    add_chunks_to_bm25(chunks, bm25_path, doc_store_path)

      
# // 30- 50 age-  100g suger 1
# // coffe hae 100 g suger

# // can i drink the coffee if 26

# // llm ()


"""

Data sources used:

    pdf:
        "backend/documents/factsheet_Prediabetes.pdf"
        "backend/documents/1452-1-3002-1-10-20180628.pdf",
        "backend/documents/Barriers_to_Optimal_Control_of_Type_2_Di.pdf",
        "backend/documents/fpsyg-05-01328.pdf",
        "backend/documents/management-of-prediabetes.pdf",
        "backend/documents/sapd-booklet.pdf",
        "backend/documents/1362.pdf",
        "backend/documents/D0211421.pdf",
        "backend/documents/file.pdf",
        "backend/documents/International Journal of Endocrinology - 2013 - Hussein - Transcultural Diabetes Nutrition Algorithm  A Malaysian.pdf",
        "backend/documents/journal.pone.0263139.pdf",
        "backend/documents/PIIS2213398423000660.pdf"


    url:
    url_list = ["https://www.webmd.com/diabetes/stop-prediabetes-progression",
    "https://www.webmd.com/diabetes/diabetes-causes",
    "https://www.webmd.com/diabetes/ss/slideshow-prediabetes-diet",    
    "https://www.webmd.com/diet/glycemic-index-diet",
    "https://www.webmd.com/diabetes/ss/slideshow-snacks-blood-sugar",

        
        
        "https://www.webmd.com/diabetes/how-sugar-affects-diabetes",
        "https://www.webmd.com/diabetes/cm/t2d-reversed-remission",
        "https://blogs.webmd.com/diabetes/20240207/5-blood-sugar-friendly-swaps-for-valentines-day",
        "https://www.webmd.com/diet/glycemic-index-diet",
        "https://www.webmd.com/diabetes/glucose-diabetes",
        "https://www.webmd.com/diabetes/causes-blood-sugar-spikes",
        "https://www.webmd.com/diabetes/features/blood-sugar-level-older-adults",
        "https://www.webmd.com/diet/news/20240911/ultra-processed-doesnt-always-mean-bad-how-to-tell",
    
        "https://gleneagles.com.my/health-digest/prediabetes",
        "https://codeblue.galencentre.org/2025/05/one-in-10-people-with-prediabetes-are-likely-to-develop-type-2-diabetes-in-a-year/"
        ]
    csv:
    1. Extract food GI from CSV
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, "documents", "GI_Table.csv")
        chunks += extract_food_gi(csv_path)


    additional manual chunks:
        "Adults between the ages of 30 and 50 should limit their sugar intake to no more than 100 grams per day.", 
        "A cup of coffee contains about 100 grams of sugar."
        "For individuals with prediabetes who are overweight or obese, a reduced calorie diet of 20–25 kcal per kilogram of body weight is recommended to achieve a weight loss of 5–10% of initial body weight within six months. To help manage blood sugar, carbohydrates should provide 45–60% of daily energy intake, protein 15–20%, and fat 25–35%. Saturated fat should be kept below 7% of total calories, and cholesterol intake should be less than 200 milligrams per day. A daily fiber intake of 20–30 grams is encouraged, while sodium should be limited to less than 2,400 milligrams per day."
        "Prediabetes is fairly common in Malaysia. A recent meta-analysis found that about 11.6% of adults have prediabetes. This suggests that more than 1 in 10 Malaysians are affected, highlighting the need for greater awareness, prevention, and management efforts."
        
        from https://www.mayoclinic.org/diseases-conditions/prediabetes/diagnosis-treatment/drc-20355284
        "Prediabetes is a condition where blood sugar levels are higher than normal but not high enough for a diabetes diagnosis. Most people with prediabetes have no clear symptoms, so it is often detected through blood tests. Early detection is important to prevent progression to type 2 diabetes.",
        "Prediabetes can be diagnosed using three main tests: fasting blood sugar test, oral glucose tolerance test, and HbA1c test. The fasting blood sugar test measures blood sugar after an overnight fast. The oral glucose tolerance test measures blood sugar after drinking a sugary solution. HbA1c reflects average blood sugar over 2-3 months.",
        "Treatment and prevention of prediabetes mainly involve lifestyle changes. Recommended strategies include healthy eating, regular physical activity, and weight management. Eating more vegetables, fruits, and whole grains while reducing processed foods and sugary drinks helps control blood sugar levels.",
        "Regular exercise is crucial in managing prediabetes. Adults are advised to aim for at least 150 minutes per week of moderate-intensity exercise, such as brisk walking, swimming, or cycling. Exercise improves insulin sensitivity and helps maintain a healthy weight.",
        "Maintaining a healthy body weight significantly reduces the risk of developing type 2 diabetes. Losing about 5-7% of body weight and combining it with regular physical activity can lower diabetes risk by 50-70%. Controlling blood pressure and cholesterol also supports overall health."
        "The exact cause of prediabetes is unknown, but family history and genetics appear to play an important role. People with prediabetes don't process sugar (glucose) properly anymore. Glucose from food enters the bloodstream, and insulin allows sugar to enter cells. When this process doesn't work properly, sugar builds up in the blood.",
        "Insulin is produced by the pancreas. When blood sugar rises after eating, insulin helps sugar enter cells. In prediabetes, the pancreas may not produce enough insulin or the cells become resistant to insulin, causing sugar to accumulate in the bloodstream.",
        "Risk factors include being overweight, large waist size, poor diet (red and processed meat, sugary drinks), physical inactivity, age over 35, family history of diabetes, race or ethnicity (Black, Hispanic, American Indian, Asian American), gestational diabetes, polycystic ovary syndrome, sleep apnea, smoking, high blood pressure, low HDL cholesterol, high triglycerides, and metabolic syndrome.",
        "Prediabetes can cause long-term damage to the heart, blood vessels, and kidneys. It can progress to type 2 diabetes, which may lead to high blood pressure, high cholesterol, heart disease, stroke, kidney disease, nerve damage, fatty liver disease, eye damage, and amputations.",
        "Healthy lifestyle choices can prevent prediabetes or slow its progression to type 2 diabetes. This includes eating healthy foods, getting active, losing excess weight, controlling blood pressure and cholesterol, and not smoking.",
        "The American Diabetes Association recommends diabetes screening for most adults starting at age 35. Adults under 35 who are overweight with additional risk factors should also be screened. People with a history of gestational diabetes should check blood sugar at least once every three years.",
        "Blood tests for prediabetes include the A1C test, fasting blood sugar test, and oral glucose tolerance test. A1C between 5.7% and 6.4% indicates prediabetes. Fasting blood sugar 100–125 mg/dL or oral glucose tolerance 140–199 mg/dL are consistent with prediabetes.",
        "Children who are overweight or obese with additional risk factors should be tested for prediabetes. Tests are recommended annually, or more often if weight changes or symptoms appear, such as increased thirst, frequent urination, fatigue, or blurred vision.",
        "Treatment focuses on healthy lifestyle changes: eating a diet high in fruits, vegetables, nuts, whole grains, and fiber, being physically active (at least 150 minutes moderate or 75 minutes vigorous activity per week), losing 5–7% of body weight, stopping smoking, and taking medications like metformin if necessary.",
        "Children with prediabetes should follow adult lifestyle recommendations: losing weight, reducing refined carbs and fats, increasing fiber, controlling portion sizes, spending at least one hour per day in physical activity, and using medication only if lifestyle changes fail."
        "Q: When should adults start diabetes screening? A: The American Diabetes Association (ADA) recommends that most adults begin screening at age 35. Screening before 35 is advised if you are overweight and have additional risk factors for prediabetes or type 2 diabetes.",

        "Q: How often should people with a history of gestational diabetes be screened? A: Health care providers usually check blood sugar levels at least once every three years.",

        "Q: What is the HbA1C (glycated hemoglobin) test? A: It shows average blood sugar over the past 2–3 months. Normal: < 5.7%. Prediabetes: 5.7%–6.4%. Diabetes: ≥ 6.5% on two separate tests. Note: The test can be inaccurate if you are pregnant or have an uncommon hemoglobin type.",

        "Q: What is the fasting blood sugar test? A: It measures blood sugar after fasting for at least 8 hours. Normal: < 100 mg/dL (5.6 mmol/L). Prediabetes: 100–125 mg/dL (5.6–6.9 mmol/L). Diabetes: ≥ 126 mg/dL (7.0 mmol/L) on two separate tests.",

        "Q: What is the oral glucose tolerance test? A: After fasting overnight, you drink a sugary liquid and your blood sugar is measured over the next 2 hours. Normal: < 140 mg/dL (7.8 mmol/L). Prediabetes: 140–199 mg/dL (7.8–11.0 mmol/L). Diabetes: ≥ 200 mg/dL (11.1 mmol/L). This test is more commonly used during pregnancy.",

        "Q: How often should people with prediabetes be retested? A: Typically once a year, to monitor for possible progression to type 2 diabetes.",

        "Q: Should children be screened for prediabetes? A: Yes. The ADA recommends testing for overweight or obese children who also have risk factors. Risk factors include family history of type 2 diabetes, high-risk race or ethnicity, low birth weight, or being born to a mother with gestational diabetes. The diagnostic ranges are the same as for adults (HbA1C: 5.7%–6.4%, fasting glucose: 100–125 mg/dL, oral glucose tolerance: 140–199 mg/dL). Children with prediabetes should be tested annually, or more often if weight changes or symptoms appear (such as increased thirst, urination, fatigue, or blurred vision)."
        "Q: When should adults start diabetes screening? A: The ADA recommends screening at age 35. If overweight and with additional risk factors, screening should begin earlier.\nData: Adults ≥35: screening recommended. Adults <35: screening if overweight + risk factors.",
        "The ADA recommends that most adults begin diabetes screening at age 35. For those under 35, earlier screening is advised if overweight and with additional risk factors for prediabetes or type 2 diabetes.",

        "Q: How often should people with a history of gestational diabetes be screened? A: Health care providers usually check blood sugar at least once every 3 years.\nData: Post-gestational diabetes: blood sugar check every 3 years.",
        "The ADA advises that individuals with a history of gestational diabetes should have their blood sugar tested at least once every three years.",

        "Q: What is the HbA1C (glycated hemoglobin) test? A: It measures average blood sugar over 2–3 months. Normal: < 5.7%. Prediabetes: 5.7%–6.4%. Diabetes: ≥ 6.5% (two tests). It may be inaccurate if pregnant or with uncommon hemoglobin.\nData: HbA1C diagnostic cutoffs included.",
        "The HbA1C test shows average blood sugar over 2–3 months. Normal: < 5.7%. Prediabetes: 5.7%–6.4%. Diabetes: ≥ 6.5% (on two separate tests).",

        "Q: What is the fasting blood sugar test? A: Done after ≥8 hours fasting. Normal: < 100 mg/dL (5.6 mmol/L). Prediabetes: 100–125 mg/dL (5.6–6.9 mmol/L). Diabetes: ≥ 126 mg/dL (7.0 mmol/L, two tests).\nData: Diagnostic ranges expressed in mg/dL and mmol/L.",
        "The fasting blood sugar test measures glucose after at least 8 hours fasting. Normal: < 100 mg/dL (5.6 mmol/L). Prediabetes: 100–125 mg/dL (5.6–6.9 mmol/L). Diabetes: ≥ 126 mg/dL (7.0 mmol/L, on two tests).",

        "Q: What is the oral glucose tolerance test? A: After fasting overnight, you drink a sugary liquid and blood sugar is tested over 2 hours. Normal: < 140 mg/dL (7.8 mmol/L). Prediabetes: 140–199 mg/dL (7.8–11.0 mmol/L). Diabetes: ≥ 200 mg/dL (11.1 mmol/L after 2h).\nData: OGTT cutoffs included.",
        "The oral glucose tolerance test involves drinking a sugary liquid after fasting overnight. Blood sugar after 2 hours: Normal: < 140 mg/dL (7.8 mmol/L). Prediabetes: 140–199 mg/dL (7.8–11.0 mmol/L). Diabetes: ≥ 200 mg/dL (11.1 mmol/L).",

        "Q: How often should people with prediabetes be retested? A: Typically once a year, to monitor progression.\nData: Annual test recommended for prediabetes.",
        "The ADA recommends that individuals with prediabetes be retested at least once a year.",

        "Q: Should children be screened for prediabetes? A: Yes. Overweight or obese children with risk factors should be tested. Risk factors: family history of type 2 diabetes, high-risk race/ethnicity, low birth weight, or maternal gestational diabetes. Same diagnostic ranges as adults. Testing annually, or more often if symptoms appear.\nData: Pediatric criteria and risk factors included.",
        "The ADA advises prediabetes testing for overweight or obese children with risk factors (family history, high-risk race/ethnicity, low birth weight, maternal gestational diabetes). Diagnostic cutoffs: HbA1C 5.7%–6.4%, Fasting 100–125 mg/dL, OGTT 140–199 mg/dL. Annual or more frequent testing if symptoms develop."

        

        from: https://www.mayoclinic.org/diseases-conditions/prediabetes/symptoms-causes/syc-20355278
        "What Is Prediabetes? Prediabetes means you have a higher than normal blood sugar level. It's not high enough to be considered type 2 diabetes yet. But without lifestyle changes, adults and children with prediabetes are at high risk to develop type 2 diabetes.",
        "Risk Factors for Prediabetes: Being overweight is a primary risk factor for prediabetes. The more fatty tissue you have — especially inside and between the muscle and skin around your abdomen — the more resistant your cells become to insulin.",
        "Prediabetes doesn't usually have any signs or symptoms. One possible sign of prediabetes is darkened skin on certain parts of the body, including the neck, armpits, and groin.",
        "Classic signs and symptoms that suggest you've moved from prediabetes to type 2 diabetes include: increased thirst, frequent urination, increased hunger, fatigue, blurred vision, numbness or tingling in the feet or hands, frequent infections, slow-healing sores, and unintended weight loss.",
        "See your healthcare provider if you're concerned about diabetes or notice any type 2 diabetes signs or symptoms. Ask about blood sugar screening if you have risk factors for diabetes.",
        "Importance of Lifestyle Changes: Eating healthy foods, making physical activity part of your daily routine, and staying at a healthy weight can help bring your blood sugar level back to normal. The same lifestyle changes that can help prevent type 2 diabetes in adults might also help bring children's blood sugar levels back to normal.",
        "Long-Term Risks of Prediabetes: If you have prediabetes, the long-term damage of diabetes — especially to your heart, blood vessels, and kidneys — may already be starting."
        "Q: What are the main risk factors for prediabetes? A: Risk factors include being overweight, having a large waist size, poor diet (e.g., red or processed meat, sugary drinks), physical inactivity, age over 35, family history of type 2 diabetes, certain ethnicities, gestational diabetes, polycystic ovary syndrome (PCOS), sleep disorders like obstructive sleep apnea, and smoking.",

        "Q: How do certain medical conditions affect prediabetes risk? A: Conditions associated with higher risk include high blood pressure, low HDL ('good') cholesterol, high triglycerides, and metabolic syndrome (a combination of obesity, high blood pressure, low HDL, high triglycerides, high blood sugar, and large waist size). These conditions can increase insulin resistance.",

        "Q: What complications can arise from prediabetes? A: Prediabetes can cause long-term damage to the heart, blood vessels, and kidneys, and may be linked to silent heart attacks. If it progresses to type 2 diabetes, additional complications include high blood pressure, high cholesterol, heart disease, stroke, kidney disease, nerve damage, fatty liver disease, eye damage, and amputations.",

        "Q: How can prediabetes be prevented? A: Preventive measures include eating healthy foods, being physically active, losing excess weight, controlling blood pressure and cholesterol, and avoiding smoking. Even with a family history of diabetes, lifestyle changes can reduce the risk of developing prediabetes or type 2 diabetes."


        from:  https://gleneagles.com.my/health-digest/prediabetes
        "What is Prediabetes - Prediabetes occurs when blood sugar levels are higher than normal but not yet at diabetic levels. It represents a critical threshold between normal blood sugar and type 2 diabetes. Adults with prediabetes often show no symptoms, despite having elevated blood sugar. Normal blood glucose levels are 70–99 mg/dL (3.9–5.5 mmol/L), while prediabetes typically ranges between 110–125 mg/dL (5.6–6.9 mmol/L).",
        "Causes of Prediabetes - Hyperglycaemia prompts pancreatic beta cells to produce more insulin. Over time, exposure to high insulin reduces receptor effectiveness, leading to worsening hyperglycaemia, metabolic disturbances, and higher risk of type 2 diabetes. In prediabetes, this process is less advanced but marks the beginning of a metabolic cascade.",
        "Signs and Symptoms - Most people with prediabetes do not display symptoms. In some cases, symptoms may include increased appetite, unexplained weight loss, elevated BMI, fatigue, sweating, blurry vision, delayed wound healing, recurring skin infections, or gum bleeding.",
        "Risk Factors - Unchangeable factors: family history of diabetes, age, and ethnicity. - Modifiable factors: overweight or obesity, sedentary lifestyle, high blood pressure, high cholesterol, polycystic ovary syndrome (PCOS), and history of gestational diabetes.",
        "Diagnosis - Prediabetes can be identified using three tests: 1. HbA1C: Normal <5.7%, Prediabetes 5.7–6.4%, Diabetes ≥6.5%. 2. Fasting blood glucose: Normal 3.9–5.5 mmol/L, Prediabetes 5.6–6.9 mmol/L, Diabetes ≥7 mmol/L. 3. Oral glucose tolerance test: Normal <7.8 mmol/L, Prediabetes 7.8–11.0 mmol/L, Diabetes ≥11.0 mmol/L.",
        "Health Risks - Prediabetes is linked with higher mortality and cardiovascular risk: 7.36 additional deaths and 8.75 more heart disease cases per 10,000 person-years over 6.6 years. Diabetes can damage major organs, cause nerve damage, and potentially lead to amputation.",
        "Treatment and Management - Prediabetes is often reversible with lifestyle changes. Many people can return blood glucose to normal and delay or prevent diabetes. Recommended strategies include: 1. Increase physical activity (≥150 min/week) 2. Eat a healthier diet with calorie restriction 3. Lose 5–10% of body weight 4. Quit smoking 5. Manage stress In some cases, Metformin may be prescribed.",
        "Prevention - Prevention includes a three-part strategy: weight loss, increased physical activity, and healthy eating. Incorporating these practices reduces risk and promotes overall health.",
        "Call to Action - Take charge of your health with lifestyle changes such as mindful eating, exercise, and timely medical advice. Screening tests and consultations at Gleneagles Hospitals can support prevention and management.",
        "Treatment and Management - Prediabetes is often reversible with lifestyle changes. Key strategies include: 1. Increase physical activity (≥150 min/week) 2. Eat a healthier diet with calorie restriction 3. Lose 5–10% of body weight 4. Quit or reduce smoking 5. Manage stress - Metformin may be prescribed in some cases. Many people can restore normal glucose levels and delay or prevent type 2 diabetes."

        from: https://www.blueshieldca.com/en/home/get-more/your-health-and-well-being/answers-to-prediabetes-questions
        "Prediabetes is a condition in which your blood sugar level is higher than normal, but not high enough to be considered type 2 diabetes. Without lifestyle changes, adults and children with prediabetes are at high risk of developing type 2 diabetes.",
        
        "Prediabetes occurs when the body cannot use insulin properly. Food is broken down into sugar, which travels through the bloodstream to provide energy. Insulin helps cells absorb sugar, but if insulin doesn't work correctly, sugar builds up in the blood, causing prediabetes.",
        
        "People who are overweight, not physically active, have a family history of diabetes, or have a history of gestational diabetes are at higher risk of developing prediabetes.",
        
        "Progression from prediabetes to type 2 diabetes is not automatic. Taking healthy steps such as losing weight, improving diet, and increasing physical activity can return blood sugar levels to the normal range.",
        
        "To reverse prediabetes, it is important to consult a healthcare provider who may recommend lifestyle changes such as weight loss, exercise, regular monitoring of blood sugar levels, and possibly medications like metformin.",
        
        "Weight loss does not need to be large to be effective. Losing 5%–7% of total body weight can significantly reduce the risk of progressing to type 2 diabetes.",
        
        "Regular physical activity is crucial. Aim for at least 150 minutes per week of moderate-intensity exercise, such as brisk walking. Always consult a doctor before starting a new exercise routine.",
        
        "Monitoring blood sugar levels, including periodic checks of A1C or oral glucose tolerance tests, helps track the effectiveness of lifestyle changes and guide further adjustments.",
        
        "Metformin may be recommended for certain individuals with prediabetes to help maintain blood sugar levels, but it is not suitable for everyone. Healthcare providers can determine if it is appropriate based on age, blood sugar readings, and other factors."


            

        from: https://www.everystepindiabetes.com/faq/
        "Q: Is prediabetes genetic or related to my lifestyle? A: Genes play a large role in prediabetes, and epigenetics are strong risk factors; however, lifestyle has a huge impact. Making healthy lifestyle changes now can help prevent diabetes in the future.",
        
        "Q: If I have prediabetes, will I eventually get diabetes? A: Not necessarily. Prediabetes can progress to type 2 diabetes if left uncontrolled, but early detection and lifestyle changes can prevent or reverse elevated blood glucose.",
        
        "Q: How do prediabetes and diabetes differ? A: The main difference lies in blood glucose levels. Fasting blood glucose between 100-125 mg/dL indicates prediabetes, while above 125 mg/dL indicates type 2 diabetes. If prediabetes is not managed, it may progress to diabetes.",
        
        "Q: What are the symptoms of prediabetes and diabetes? A: Prediabetes usually has no visible symptoms. Some people may show diabetes symptoms such as frequent urination, extreme thirst, excessive hunger, tiredness, blurred vision, or numbness/tingling in hands or feet.",
        
        "Q: Who is at risk of developing prediabetes? A: People at higher risk include those who are overweight, physically inactive, aged 35 or older, have a family history of type 2 diabetes, history of gestational diabetes, certain ethnic groups, high blood pressure, abnormal cholesterol/triglyceride levels, or have polycystic ovary syndrome (PCOS).",
        
        "Q: What can you do if you think you are prediabetic? A: Visit a doctor. Lifestyle interventions such as increasing physical activity, eating a balanced diet, and losing weight can help control blood sugar. Medications may be considered if lifestyle changes alone are insufficient.",
        
        "Q: How do you test for prediabetes? A: Doctors can check medical history, perform a physical exam, and run blood tests such as fasting plasma glucose (FPG), haemoglobin A1c (HbA1c), or oral glucose tolerance test (OGTT). Usually one or two tests are done.",
        
        "Q: Who should I contact to learn more about prediabetes? A: You should contact your healthcare provider to assess your risk and get advice on prevention and management of prediabetes.",
        
        "Q: Can people with diabetes play sports? A: Yes. Exercise is encouraged for people with diabetes as part of a healthy lifestyle, which helps reduce risk of complications. Consult a healthcare professional before starting new exercise routines.",
        
        "Q: What can you eat if you have diabetes? A: You can eat most foods by managing portion sizes and carbohydrate intake. A dietitian can help with meal planning and carbohydrate counting specific to your needs.",
        
        "Q: Why does it matter if my blood sugar is 120 or 200? A: Keeping blood sugar under control is crucial. High blood sugar can damage veins and arteries, increasing risk of heart attacks, strokes, kidney disease, neuropathies, and vision problems.",
        
        "Q: What foods have carbohydrates? A: Carbohydrates are in fruits, starchy vegetables, milk, yogurt, rice, cereals, bread, grains, and many snacks or sweets. Check nutrition labels to determine carbohydrate content.",
        
        "Q: Do I need to follow a low-carb diet? A: Not necessarily. Watch portion sizes and prioritize carbs from fruits, vegetables, whole grains, and low-fat dairy. Lower fat, high-fiber foods and maintaining healthy calories are also important.",
        
        "Q: If it is sugar-free, can I eat as much as I want? A: No. Sugar-free foods may still contain carbohydrates, calories, or fat, which can affect blood sugar. Always read nutrition labels and consume in moderation.",
        
        "Q: Will taking the COVID-19 vaccine affect my diabetes? A: Blood sugar may rise temporarily for a few days after vaccination. Monitor your blood glucose and follow usual sick day rules. Stay hydrated and have support if needed."


        FROM https://www.uhc.com/news-articles/healthy-living/surprising-signs-of-prediabetes-and-risk-factors
        "Q: How does prediabetes differ from type 2 diabetes? A: Prediabetes has elevated blood sugar levels but not as high as type 2 diabetes. Type 2 diabetes occurs when the body can't properly use or produce insulin, leading to chronic high blood sugar and potential long-term complications.",

        "Q: What are early signs of prediabetes? A: Prediabetes usually has no obvious symptoms. Some early warning signs may include darkened skin or skin tags in certain areas, unexplained weight loss or gain, increased appetite, and fatigue or general weakness.",

        "Q: What are risk factors for prediabetes? A: Risk factors include being overweight, age 45 or older, family history of type 2 diabetes, low physical activity, history of gestational diabetes, certain ethnic backgrounds, and polycystic ovary syndrome (PCOS).",

        "Q: How can I lower my risk of prediabetes? A: Lifestyle changes such as eating non-starchy vegetables, lean proteins, whole grains, limiting sugary drinks, maintaining at least 150 minutes of physical activity weekly, reaching a healthy weight, managing stress, and getting 7+ hours of sleep nightly can reduce risk.",

        "Q: How is prediabetes diagnosed? A: Prediabetes can be identified through blood tests including the A1C test (average blood sugar over 2-3 months), fasting blood glucose test, and glucose tolerance test. Results above normal but below diabetes thresholds indicate prediabetes.",

        "Q: What should I do if I am prediabetic? A: Consult a doctor to review your risk factors. Lifestyle interventions such as healthy eating, regular exercise, weight management, stress reduction, and proper sleep can help manage blood sugar. In some cases, medication may be recommended."

        
        from: https://www.sunwaymedical.com/en/in-the-news/recognising-prediabetes-symptoms-key-to-preventing-diabetes
        "Q: What are the symptoms of prediabetes? A: Prediabetes usually has no obvious symptoms. When symptoms occur, they may include frequent urination, fatigue, blurred vision, numbness in the hands or feet, slow-healing wounds, unexpected weight changes, and darkened skin patches on the neck, armpits, or groin.",

        "Q: Why is managing prediabetes important? A: Managing prediabetes is crucial because if left uncontrolled, it increases the risk of developing type 2 diabetes, which can cause serious complications in the heart, kidneys, blood vessels, and other organs.",

        "Q: What causes type 2 diabetes? A: Type 2 diabetes occurs when the body cannot produce enough insulin or cannot use insulin effectively. Insulin regulates blood sugar levels, and insulin resistance or deficiency can lead to high blood sugar and long-term organ damage.",

        "Q: What are the risk factors for developing prediabetes? A: Risk factors include being overweight or obese, low physical activity, family history of diabetes, gestational diabetes, unhealthy diet, and certain conditions like polycystic ovary syndrome (PCOS). Children and young people with obesity are also at higher risk.",

        "Q: How can prediabetes be prevented or managed? A: Lifestyle interventions such as maintaining a healthy weight, engaging in regular physical activity (at least 150 minutes per week), eating a balanced diet with fewer sugary foods and refined carbohydrates, and monitoring blood sugar levels can help prevent or manage prediabetes.",

        "Q: Should children be monitored for prediabetes? A: Yes. Children who are overweight, have a family history of diabetes, or exhibit risk factors should have blood tests for early detection. Early lifestyle interventions can prevent progression to type 2 diabetes.",

        "Q: Can prediabetes be cured? A: Prediabetes cannot be 'cured,' but it can be managed and sometimes reversed with proper health and lifestyle practices, reducing the risk of developing type 2 diabetes."



        from: https://www2.hse.ie/conditions/pre-diabetes/
        "Q: Who is at risk of prediabetes? A: You are more at risk if you are over 45, have a close relative with diabetes, are overweight or obese, had gestational diabetes during pregnancy, are physically inactive, have high blood pressure, high cholesterol, low HDL, high triglycerides, history of heart disease, require long-term steroid use, belong to certain ethnicities (South Asian, Chinese, Hispanic, African, Caribbean, black African), have haemochromatosis, or are a woman with polycystic ovary syndrome.",

        "Q: How is prediabetes diagnosed? A: Doctors use a blood test called HbA1c to check blood glucose levels. Results show: no diabetes if less than 42 mmol/mol, prediabetes if 42 to 47 mmol/mol, and type 2 diabetes if 48 mmol/mol or higher.",

        "Q: What will your GP or nurse discuss if you are diagnosed with prediabetes? A: They will explain what prediabetes is, your risk of developing type 2 diabetes, the impact of high blood glucose, healthy eating, being active, losing weight, possible medicines for cholesterol or blood pressure, and lifestyle choices such as smoking and alcohol use.",

        "Q: How is prediabetes treated? A: Treatment includes being more active, reducing sitting time, losing weight, eating healthy food, and attending regular check-ups. Acting early helps prevent type 2 diabetes.",

        "Q: What is the Diabetes Prevention Programme? A: It is a free 12-month group course available online or in person. It helps people with prediabetes make healthy lifestyle changes. A GP can refer you to the programme.",

        "Q: How does physical activity help with prediabetes? A: Being active lowers blood glucose, blood pressure, and cholesterol, helps manage weight, and reduces the risk of type 2 diabetes.",

        "Q: How does managing weight help with prediabetes? A: Maintaining a healthy weight delays or prevents type 2 diabetes. Losing 5–7% of body weight can significantly reduce the risk.",

        "Q: How does waist size affect prediabetes risk? A: Carrying excess weight around the tummy increases diabetes risk, even if BMI is not high. Risk increases if men have a waist of 94cm (37 inches) or more, or 90cm (35 inches) for Asian men, and women with a waist of 80cm (31.5 inches) or more.",


        "Diagnosing is done through a blood test called HbA1c, which measures blood glucose levels. Results show no diabetes if less than 42 mmol/mol, prediabetes if between 42 and 47 mmol/mol, and type 2 diabetes if 48 mmol/mol or higher. What your GP or nurse discusses will depend on your test results, your risk of developing type 2 diabetes, and any other medical conditions. If diagnosed with prediabetes, you should ask your doctor about its meaning for your health, your risk of type 2 diabetes, the impact of high blood glucose, lifestyle changes such as eating well, being active, losing weight, and whether medicines are needed to treat other risks like high cholesterol or high blood pressure."


        FROM https://pmc.ncbi.nlm.nih.gov/articles/PMC4360422/
        # Prevalence
        "Prevalence of prediabetes is increasing in both developed and developing countries. According to the CDC National Diabetes Statistics Report, 37% of U.S. adults over 20 and 51% of those over 65 had prediabetes between 2009 and 2012, defined by fasting glucose or HbA1c levels. This translated to nearly 86 million adults with prediabetes in the United States alone in 2012. Globally, the prevalence of impaired glucose tolerance (IGT) in 2010 was estimated at 343 million people, or 7.8% of the world’s population, with regional variation from 5.8% in South East Asia to 11.4% in North America and the Caribbean. The International Diabetes Federation projects that the global prevalence of prediabetes will rise to 471 million by 2035.",
        "Q: What is the prevalence of prediabetes? A: Prediabetes affects around 37% of U.S. adults over 20 and 51% of those over 65, representing nearly 86 million Americans in 2012. Globally, about 343 million people (7.8% of the population) had impaired glucose tolerance in 2010, and the number is projected to rise to 471 million worldwide by 2035.",

        # Health risks
        "Health risks associated with prediabetes include progression to type 2 diabetes, kidney disease, neuropathies, retinopathy, and macrovascular disease. The risk of progression to diabetes varies with the criteria used to define prediabetes: annual incidence rates range from 4% to 6% for isolated impaired glucose tolerance (IGT), 6% to 9% for isolated impaired fasting glucose (IFG), and 15% to 19% when both are present. Nephropathy and early kidney disease have been linked to prediabetes, although whether this is causal remains debated. Neuropathy findings include reduced heart rate variability, decreased parasympathetic modulation, erectile dysfunction, painful sensory neuropathy, and small fiber neuropathy. Retinopathy has been observed in nearly 8% of participants with prediabetes in the Diabetes Prevention Program. Macrovascular risks include increased prevalence of coronary heart disease, although shared risk factors with diabetes may play a role. Overall, prediabetes is associated with multiple complications that can occur even before the onset of overt diabetes.",
        "Q: What health risks are associated with prediabetes? A: Prediabetes can lead to progression to type 2 diabetes, kidney disease, neuropathies (such as nerve dysfunction and erectile dysfunction), retinopathy, and macrovascular disease like coronary heart disease. These risks may occur even before diabetes develops.",

        # Treatment
        "Treatment of prediabetes is focused on lifestyle interventions and, in some cases, pharmacotherapy or bariatric surgery. Lifestyle interventions such as increased physical activity, dietary changes, and weight loss have been shown to reduce the risk of progression to diabetes by more than 50%. Pharmacological treatments studied include metformin, thiazolidinediones, alpha-glucosidase inhibitors, GLP-1 analogs, and anti-obesity drugs such as orlistat. Metformin can reduce diabetes risk by about 45%, though lifestyle change remains more effective in most studies. Bariatric surgery, including gastric bypass and sleeve gastrectomy, has been shown to result in sustained weight loss and up to 75% reduction in diabetes risk in obese adults. Overall, lifestyle changes remain the cornerstone of treatment, but medications and surgery may be considered for high-risk individuals.",
        "Q: What are the treatment options for prediabetes? A: Treatment includes lifestyle interventions such as diet, exercise, and weight loss, which can reduce diabetes risk by more than 50%. Medications such as metformin, thiazolidinediones, alpha-glucosidase inhibitors, GLP-1 analogs, and orlistat may also help. For obese individuals, bariatric surgery can significantly reduce the risk of developing diabetes."
        
        "Diagnosis of prediabetes is based on criteria that vary between organizations. The World Health Organization (WHO) defines it as intermediate hyperglycemia, using impaired fasting glucose (FPG 6.1–6.9 mmol/L or 110–125 mg/dL) and impaired glucose tolerance (2 h plasma glucose 7.8–11.0 mmol/L or 140–200 mg/dL after a 75 g oral glucose load). The American Diabetes Association (ADA) uses the same cut-off for impaired glucose tolerance but a lower threshold for impaired fasting glucose (100–125 mg/dL) and includes HbA1c levels of 5.7–6.4%. However, studies show poor correlation between HbA1c, IFG, and IGT, and these tests often have limited reproducibility. While HbA1c may better reflect average glucose, it is influenced by genetic factors and may not always be precise. Overall, prediabetes represents an overlapping group of individuals with one or more abnormalities in glucose metabolism, and having both IFG and IGT usually indicates more advanced impairment of glucose regulation."


        "Treatment of prediabetes aims to prevent the development of diabetes, prevent complications of diabetes, and prevent complications of prediabetes itself."

        "Research shows that lifestyle and drug-based interventions for prediabetes can reduce the incidence of diabetes and lower stroke risk, but evidence for reducing all-cause mortality, cardiovascular death, or myocardial infarction is limited."

        "The CDQDPS study with lifestyle intervention and 20-year follow-up showed nearly 50% relative risk reduction in severe retinopathy, but no significant difference in neuropathy or nephropathy."

        "The Malmo Preventive Project suggested reduced mortality with long-term lifestyle intervention focusing on diet and physical activity, but it was not a randomized trial."

        "Most evidence supports lifestyle interventions such as dietary modification and physical activity as the foundation of therapy for prediabetes."

        "Pharmacotherapy, especially metformin, shows positive outcomes and is recommended by ADA for certain high-risk individuals, but long-term endpoints remain undefined."

        "In children with prediabetes, the concept of treatment is not systematically studied. The long-term safety and efficacy of pharmacotherapy remain uncertain, and puberty-related insulin resistance complicates risk estimates."

        "Q: What is the rationale for treatment of prediabetes? A: The rationale includes prevention of diabetes, prevention of complications of diabetes, and prevention of complications of prediabetes itself."

        "Q: Do interventions for prediabetes reduce the risk of complications? A: Lifestyle and drug interventions reduce diabetes incidence and stroke risk, but evidence for reducing overall mortality or major cardiovascular events is inconsistent."

        "Q: What do studies show about microvascular complications? A: The CDQDPS study showed reduced severe retinopathy but no difference in neuropathy or nephropathy risk."

        "Q: What are the pros of lifestyle interventions? A: They are safe, effective in preventing diabetes, and supported by most guidelines."

        "Q: What are the cons of lifestyle interventions? A: They are often not reimbursed by healthcare insurance plans."

        "Q: What are the pros of pharmacotherapy such as metformin? A: Metformin has a favorable long-term safety profile and positive outcomes, and ADA recommends it for certain high-risk individuals."

        "Q: What are the cons of pharmacotherapy for prediabetes? A: Long-term benefits on complications are unclear, the endpoint of therapy is undefined, and in children safety and efficacy data are lacking."


        from: https://www.hopkinsmedicine.org/health/wellness-and-prevention/prediabetes-diet
        "Prediabetes can often be controlled or even reversed through healthy diet and lifestyle. A balanced approach to diet is essential, with the Mediterranean diet considered the gold standard. Key elements include whole grains, lean protein, healthy fats, and plenty of nonstarchy vegetables.",
        "The American Diabetes Association meal plan recommends filling 50% of the plate with nonstarchy vegetables such as leafy greens, 25% with healthy carbohydrates like brown rice, quinoa, or farro, and 25% with lean protein such as chicken, fish, turkey, or tofu. Water or zero-calorie beverages are preferred.",
        "The World Health Organization advises limiting added sugars to less than 10% of total daily energy intake, ideally below 5%. For a 2,000-calorie diet, this equals 50 g (12 teaspoons) at the 10% level, or 25 g (6 teaspoons) at the 5% level.",
        "The American Heart Association recommends stricter limits for people at risk of heart disease, including prediabetes: no more than 25 g (6 teaspoons) per day for women, and 36 g (9 teaspoons) per day for men. One can of soda contains about 32 g (8 teaspoons) of sugar, nearly a full day’s limit.",
        "The '5-20 Rule' for nutrition labels suggests choosing products with 5% or less daily sugar value, and avoiding those with 20% or more.",
        "Grapefruit and pomegranate juice can interact with medications processed by cytochrome P450. High-dose supplements of ginseng, gingko, or garlic may lower blood sugar and should only be taken with professional guidance.",
        "Because everyone is different, prediabetes meal plans should be tailored individually. For example, patients with high cholesterol may need lower fat, while those with high A1C may benefit from lower carbohydrate intake. Consulting a registered dietitian is recommended."
        "Q: How to prevent prediabetes? A: Prediabetes can be prevented or reversed with healthy lifestyle changes such as adopting a Mediterranean diet, exercising regularly, losing excess weight, controlling blood pressure and cholesterol, limiting added sugars (less than 25–50 g/day depending on guidelines), and avoiding smoking.",
        "Q: What foods should I eat if I have prediabetes? A: Choose whole grains, lean protein, healthy fats, and nonstarchy vegetables. The ADA recommends filling half the plate with vegetables, one-quarter with healthy carbs, and one-quarter with lean protein. Water or zero-calorie drinks are preferred.",
        "Q: What should I eat for breakfast if I have prediabetes? A: Opt for meals with lean protein, low-fat dairy, and fiber. Good options include high-fiber cereal (at least 5 g per serving), whole fruit, vegetables, and whole grains. If skipping breakfast, a low-carb meal replacement bar or shake may help.",
        "Q: What fruits should I avoid with prediabetes? A: All fruits are generally safe. Whole fresh fruit provides both fiber and natural sugar, which is healthier than fruit juice. However, avoid pomegranate and grapefruit juice if taking certain medications.",
        "Q: How much sugar is too much for people with prediabetes? A: WHO recommends less than 50 g (12 teaspoons) per day, ideally under 25 g (6 teaspoons). The AHA recommends less than 25 g for women and less than 36 g for men daily. A single soda can contains about 32 g (8 teaspoons), nearly a full day’s allowance.",
        "Q: Why is professional guidance important for prediabetes diet? A: Since prediabetes often coexists with other conditions like high cholesterol or high blood pressure, meal plans should be individualized. A doctor or dietitian can tailor diet and lifestyle strategies to each person’s health profile."

    

        FROM: https://healthunmuted.com/blog/six-questions-to-ask-your-healthcare-provider-if-you-are-diagnosed-with-prediabetes
        "An A1C test measures the average blood sugar level over approximately three months. Results below 5.7% are considered normal, 5.7%–6.4% indicate prediabetes, and 6.5% or above indicates diabetes. Your healthcare provider may repeat the test or run additional tests to confirm the diagnosis.",
        "Maintaining a healthy weight significantly reduces the risk of developing type 2 diabetes. Healthcare providers can recommend safe and sustainable strategies for weight loss, such as gradual lifestyle changes, regular physical activity, and setting realistic goals for long-term maintenance.",
        "Dietary changes are crucial for reducing prediabetes risk. Providers can guide patients on foods to eat more often (whole grains, lean protein, vegetables, healthy fats) and foods to limit (refined carbs, added sugars, processed foods). Resources are also available for people facing budget concerns.",
        "Medication may help manage related health risks such as high blood pressure or high cholesterol. Metformin, in particular, is sometimes recommended for people with prediabetes who are at high risk of progressing to type 2 diabetes.",
        "Support programs provide structured education and lifestyle support. Examples include the CDC’s National Diabetes Prevention Program, ImpactDiabetes.org, and community-based programs by organizations such as the American Diabetes Association. These programs are available in multiple formats including online, in-person, and telehealth."
        "Important questions to ask your healthcare provider about prediabetes include: 1) What is my A1C, and what does it mean? 2) What signs and symptoms should I look out for? 3) What are some healthy ways to lose weight and keep it off? 4) What changes should I make to my diet? 5) Could medication be right for me? 6) How can I find a type 2 diabetes prevention program? These questions help guide conversations with your doctor and support prevention of type 2 diabetes."
        "Q: What questions should I ask my healthcare provider about prediabetes? A: Ask these six key questions: 1) What is my A1C, and what does it mean? 2) What signs and symptoms should I look out for? 3) What are some healthy ways to lose weight and keep it off? 4) What changes should I make to my diet? 5) Could medication be right for me? 6) How can I find a type 2 diabetes prevention program? These questions help you understand your current health and take proactive steps to reduce your risk of type 2 diabetes.",
        "Q: What is my A1C, and what does it mean? A: The A1C test shows your average blood sugar over the last 3 months. Below 5.7% is normal, 5.7%–6.4% indicates prediabetes, and 6.5% or higher indicates diabetes. Your provider may order repeat or confirmatory tests to ensure accuracy.",
        "Q: What are some healthy ways to lose weight and keep it off? A: Sustained weight loss reduces the risk of type 2 diabetes. Your healthcare provider can recommend a personalized plan including safe calorie reduction, increased daily activity, and long-term strategies for weight maintenance instead of quick fixes.",
        "Q: What changes should I make to my diet? A: Providers can help design a balanced meal plan focusing on whole grains, lean proteins, healthy fats, and nonstarchy vegetables while limiting refined carbohydrates, sugary drinks, and processed snacks. If affordability is an issue, they may suggest community or government resources.",
        "Q: Could medication be right for me? A: Some people with prediabetes may benefit from medication, especially if they also have high blood pressure, high cholesterol, or a higher risk of developing diabetes. Metformin is commonly prescribed. Your provider will discuss risks, benefits, and whether your insurance covers it.",
        "Q: How can I find a type 2 diabetes prevention program? A: Options include the CDC’s National Diabetes Prevention Program, ImpactDiabetes.org, and community programs offered by groups like the American Diabetes Association. Many programs are available online, in-person, or through telehealth, offering flexibility to fit your schedule."

        

        from: https://dietitiansaustralia.org.au/health-advice/low-carbohydrate-diets-people-type-1-and-type-2-diabetes
        "A low-carbohydrate diet can be defined by how many grams of carbohydrates are eaten per day. Very low (ketogenic) is 20-50g/day, low is less than 130g/day, moderate is 130-230g/day, and high is more than 230g/day. Carbohydrates are an important source of energy, vitamins, minerals, fibre, and fuel for the brain. Choosing high-fibre, nutrient-rich carbs like wholegrains, legumes, fruits, and vegetables is recommended.",

        "The primary goal of diabetes management, including for people with prediabetes, is to maintain blood glucose levels as close to target range as possible. Management also aims to protect the heart and blood vessels by controlling blood fats and blood pressure. For type 2 diabetes and prediabetes, weight management can also help improve health outcomes.",
        
        "Research suggests that adults with type 2 diabetes who are overweight or obese may follow a low-carb diet safely for up to 6 months. This can improve fasting blood glucose, HbA1c, and triglyceride levels. However, evidence for long-term benefits beyond 12-24 months is inconsistent.",
        
        "Weight loss results from low-carb diets are mixed. Some studies show greater weight loss in the short term, but others show no difference compared to moderate- or high-carb diets. Benefits tend to appear in the first few months but not necessarily in the long term. Weight loss is not guaranteed on a low-carb diet if total energy intake is not reduced.",
        
        "There is no consistent evidence that low-carb diets are more effective than other diets for long-term blood glucose and heart health. For people with type 2 diabetes or prediabetes who are overweight, different eating patterns can lead to similar results if they reduce overall energy intake.",
        
        "When reducing carbohydrates, people usually replace them with more protein or fat. Low-carb high-fat diets should focus on healthy fats such as nuts, avocado, olive oil, and oily fish. Unhealthy fats like processed meats, deep-fried foods, and coconut oil should be avoided. Low-carb high-protein diets should focus on lean protein, eggs, fish, legumes, and soy products.",
        
        "There is no single best diet for people with diabetes or prediabetes. A variety of eating patterns can be effective. Individualised advice from an Accredited Practising Dietitian (APD) is important to ensure nutritional balance, sustainability, and personalisation based on health status and lifestyle.",
        
        "Some people with type 2 diabetes may achieve remission with a low-carb diet, but this is not possible for everyone. Studies show that remission is more likely in people diagnosed within 5 years, not taking insulin, and who lose 10-15% of body weight. Remission may not last if the diet is not maintained.",
        
        "Low-carb diets are not recommended for certain groups such as children, pregnant or breastfeeding women, people with kidney disease, or people at risk of eating disorders. Those taking SGLT-2 inhibitor medications should avoid ketogenic diets. Medical guidance is essential.",
        
        "People on insulin or glucose-lowering medications are at higher risk of hypoglycaemia (low blood sugar) when following a low-carb diet. Healthcare providers may need to adjust medication dosages. This applies to people with prediabetes who may be starting medication as well.",
        
        "Example low-carb menu includes: Breakfast with eggs, spinach, avocado, feta on wholegrain toast; Lunch with tuna salad and a slice of wholegrain bread; Dinner with baked chicken and vegetables. Snacks can include nuts, Greek yoghurt with berries, or hummus with carrot sticks."

        "Q: Do people with prediabetes need to follow a low-carb diet? A: Not necessarily. Low-carb diets may help improve blood glucose in the short term, especially if you are overweight. However, they are not the only option, and other balanced diets can achieve similar results. The key is reducing overall energy intake, eating nutritious foods, and getting support from your healthcare team.",
        
        "Q: Can I eat unlimited amounts of sugar-free foods if I have prediabetes? A: No. Even sugar-free foods may contain calories, unhealthy fats, or sugar substitutes that affect your health. Eating them in unlimited amounts may prevent weight management and healthy blood sugar control. Moderation is still important.",
        
        "Q: What is the role of carbohydrates in prediabetes? A: Carbohydrates provide fibre, vitamins, and minerals, and are the main energy source for the body and brain. Choosing high-fibre carbs like legumes, wholegrains, and vegetables is important for people with prediabetes.",
        
        "Q: Is weight loss guaranteed if I follow a low-carb diet for prediabetes? A: No. Weight loss only happens if you reduce overall energy intake. Some people lose weight on low-carb diets, but others do not. A low-carb diet is not automatically effective for weight management.",
        
        "Q: Can prediabetes go into remission with a low-carb diet? A: Some people with type 2 diabetes may achieve remission, but for prediabetes the main goal is prevention. Weight management, healthy eating, and regular exercise are the most effective strategies to prevent progression to type 2 diabetes.",
        
        "Q: Who should avoid a low-carb diet, even with prediabetes? A: Children, pregnant or breastfeeding women, people with kidney disease, or people at risk of eating disorders should not follow a low-carb diet. Always consult your doctor or dietitian before making big dietary changes.",
        
        "Q: What questions should I ask my healthcare provider about low-carb diets and prediabetes? A: You can ask: (1) Is a low-carb diet safe for me? (2) How many carbs should I eat each day? (3) Do I need to adjust my medications? (4) What are healthier carb options for me? (5) How do I make sure I get enough nutrients?",

        

        from https://www.homage.com.my/health/malaysian-food-for-diabetics/
        "In Malaysia, diabetes is a major public health issue. According to the National Health Morbidity Survey (NHMS) 2019, 1 in 5 Malaysian adults aged 18 and above have diabetes. That equals 3.9 million Malaysians. Diabetes is much more common among adults aged 50 and above.",
        
        "Diabetes is a chronic condition that occurs when the pancreas produces insufficient insulin, or when the body cannot effectively use insulin. Insulin regulates blood sugar by converting glucose into energy. Disruption in this process can cause hyperglycemia and long-term damage to organs and systems.",
        
        "There are two main types of diabetes: Type 1, where the body does not produce insulin (usually diagnosed in children, teenagers, and young adults), and Type 2, where the body does not use insulin properly (most common in adults). Prediabetes is when blood sugar is higher than normal but not yet in the diabetes range, and it places people at high risk for developing type 2 diabetes.",
        
        "Many Malaysians lack awareness of diabetes. Surveys show that 52% of respondents do not know diabetes cannot be cured, 51% think it is not difficult to manage, and 37% of people with diabetes do not know what abnormal blood sugar readings are.",
        

        "Food plays a central role in diabetes prevention and management. High-calorie diets, excessive sugar, and refined carbohydrates are major contributors to diabetes risk. A balanced and nutritious diet, portion control, and regular physical activity can help reduce blood glucose, promote weight loss, and improve insulin sensitivity.",
        
        "Carbohydrates have the strongest effect on blood glucose. Foods and drinks with high glycemic index, such as fruit juice, can raise blood sugar quickly compared to whole fruits. Monitoring carbohydrate intake is crucial for people with diabetes and prediabetes.",
        
        "Diabetes burnout can occur when people feel overwhelmed or frustrated about managing blood glucose. This can cause a loss of motivation to monitor health. Support from family, friends, and healthcare professionals is important.",
        

        "A balanced diet for diabetes and prediabetes should include whole grains, fruits, vegetables, low-fat dairy, lean proteins like fish and chicken, and sufficient water. Intake of fats, oils, sugars, and salt should be reduced. Regular meal intervals and portion control help regulate appetite, prevent overeating, and support weight management.",
        
        "The Malaysian Healthy Plate recommends: one-quarter carbohydrates (e.g. rice, bread), one-quarter proteins (e.g. fish, tofu, meat), and half vegetables. Fruits should be limited to one cup or the size of a small rice bowl per serving.",
        

        "Foods that should be limited in Malaysia include: kuih-muih (sweet local desserts), keropok lekor and fried snacks, teh tarik (sweet milk tea), roti canai (fried flatbread), white rice, candy, and sweetened coffee. These foods are high in sugar, unhealthy fats, or have a high glycemic index.",
        

        "Healthier alternatives include: fruits instead of fruit juice, brown or whole grain rice instead of white rice, whole grain bread or capati instead of roti canai, vegetables as a daily staple, plain yoghurt instead of sweetened yoghurt, and unsweetened tea instead of sweetened beverages."
        "Q: How common is diabetes in Malaysia? A: According to NHMS 2019, 1 in 5 adults aged 18 and above have diabetes. That equals 3.9 million Malaysians, with the condition being more common in people aged 50 and above.",
        
        "Q: What is prediabetes? A: Prediabetes is when blood sugar is higher than normal but not high enough for a diabetes diagnosis. It increases the risk of developing type 2 diabetes, heart disease, and stroke. Lifestyle changes like healthier eating and physical activity can prevent progression.",
        
        "Q: Do people with prediabetes in Malaysia need to avoid their favourite local foods? A: No, but portion control and moderation are essential. Popular foods like kuih-muih, teh tarik, and roti canai are high in sugar or fat. They should be eaten less often or in smaller amounts. Healthier swaps like brown rice, whole grain bread, fruits, and vegetables are better choices.",
        
        "Q: What is the Malaysian Healthy Plate, and how does it help with prediabetes? A: The Healthy Plate guideline recommends one-quarter carbohydrates, one-quarter protein, and half vegetables. It encourages portion control and balanced nutrition, which help manage blood glucose and prevent diabetes.",
        
        "Q: Why is white rice a risk factor for prediabetes? A: White rice has a high glycemic index and raises blood sugar quickly. Studies show people who eat a lot of white rice have a 27% higher risk of developing type 2 diabetes. Brown rice and whole-grain rice are healthier alternatives.",
        
        "Q: Can Malaysians with prediabetes drink teh tarik? A: Teh tarik is high in sugar and condensed milk, making it unhealthy for blood sugar control. People with prediabetes should limit or avoid it, or switch to unsweetened tea instead.",
        
        "Q: What should Malaysians with prediabetes eat instead of sweets and snacks? A: Choose whole fruits instead of fruit juice or candy, whole grain bread instead of white bread, plain yoghurt with fruit instead of sweetened yoghurt, and nuts or vegetables as snacks.",
        
        "Q: What lifestyle changes help with prediabetes in Malaysia? A: Following a balanced diet, reducing high-sugar and fried foods, practicing portion control, engaging in regular physical activity, and monitoring blood glucose are the main strategies to prevent diabetes progression.",
        
        "Q: Can prediabetes cause emotional stress? A: Yes. Some people feel frustrated or burned out from constantly monitoring their health. This is called diabetes burnout. Emotional support from family, friends, or healthcare providers is important for managing both physical and mental health."



        from:https://www.healthline.com/health/diabetes/prediabetes-diet
    
        "Prediabetes is characterized by higher-than-normal fasting blood sugar or higher-than-normal blood sugar after eating. It is often the result of insulin resistance, where the body does not use insulin properly. People with prediabetes are at increased risk of developing type 2 diabetes and cardiovascular disease.",

        "Prediabetes does not always progress to type 2 diabetes. Early lifestyle changes such as healthy eating, physical activity, and portion control can help bring blood sugar back to normal levels.",

        "In prediabetes, sugar from food builds up in the bloodstream because insulin cannot easily move it into cells. The type and amount of carbohydrates consumed greatly affect blood sugar. Refined and processed carbohydrates cause higher spikes, while fiber and whole grains help stabilize glucose levels.",

        # Tip 2: Carbohydrate Intake
        "Monitoring carbohydrate intake is important for prediabetes. Foods with high glycemic index (GI) raise blood sugar quickly, while low GI foods such as beans, non-starchy vegetables, sweet potatoes, and nuts are better options. Cooking methods, food combinations, and portion size also affect GI impact.",

        "Medium GI foods like corn, brown rice, whole wheat bread, and oats can be eaten in moderation. High GI foods such as white bread, russet potatoes, soda, and juice should be limited.",

        # Tip 3: Portion Sizes
        "Controlling portion size is essential. Overeating carbohydrates, even healthy ones, can raise blood sugar. Reading food labels, practicing mindful eating (eating slowly, avoiding distractions, paying attention to hunger cues) can help prevent overeating.",

        "A 2018 study found that very low-carb diets (under 40% of calories) and high-carb diets (above 70%) are both linked with increased mortality risk. A moderate intake of 50–55% carbohydrates, spread evenly throughout the day, is associated with lower risk.",

        # Tip 4: Protein
        "Lean proteins help manage blood sugar and reduce unhealthy fat intake. Good options include beans, legumes, tofu, tempeh, low-fat Greek yogurt, eggs, chicken, turkey, fish (cod, tuna, trout), shellfish, and lean beef cuts. Avoid meats high in visible fat. Note that some protein sources, like beans and yogurt, also contain carbs.",

        # Tip 5: Alcohol
        "Alcohol should be consumed in moderation. Women should limit to 1 drink per day, men to 2. Drinks like beer, wine, or spirits are best consumed without sugary mixers. Alcohol can cause dehydration and affect blood sugar levels.",

        # Tip 6: Water
        "Water is the best choice for hydration in prediabetes. Sugary sodas, juices, and energy drinks add quick-digesting carbohydrates and can spike blood sugar. For variety, water can be flavored with lemon, lime, cucumber, or mint.",

        # Tip 7: Exercise
        "Exercise is essential for managing prediabetes. Physical activity improves insulin sensitivity and helps muscles use glucose for energy. Guidelines recommend 150–300 minutes of moderate aerobic activity or 75–150 minutes of vigorous activity weekly, plus 2–3 sessions of resistance training. Even simple activities like walking, dancing, or cycling help reduce risk. Avoid sitting for more than 30 minutes at a time.",

        "Prediabetes does not have to develop into type 2 diabetes. Eating plenty of fiber, monitoring carbs, controlling portions, choosing lean proteins, limiting alcohol, drinking water, and exercising regularly are key strategies for maintaining healthy blood sugar levels."

            "Q: Does prediabetes always lead to type 2 diabetes? A: No. With early lifestyle changes such as healthy eating, exercise, and weight management, it is possible to reverse prediabetes or prevent it from progressing.",

        "Q: How should people with prediabetes manage carbohydrates? A: Focus on low-GI foods such as non-starchy vegetables, beans, sweet potatoes, and nuts. Limit high-GI foods like white bread, soda, and juice. Portion control is essential.",

        "Q: Do people with prediabetes need to avoid all carbs? A: No. Carbohydrates should make up about 50–55% of daily calories, spread evenly across meals. Very low-carb and very high-carb diets may both increase health risks.",

        "Q: What protein foods are best for prediabetes? A: Lean proteins such as chicken, turkey, fish, tofu, legumes, low-fat yogurt, and lean cuts of beef. These support satiety and reduce intake of unhealthy fats.",

        "Q: Is alcohol safe for people with prediabetes? A: Yes, in moderation. Women should have no more than 1 drink per day, men no more than 2. Avoid sugary cocktails and drink water to prevent dehydration.",

        "Q: Why is water important for prediabetes? A: Water helps prevent dehydration and avoids the blood sugar spikes caused by sugary drinks like soda and juice.",

        "Q: How much exercise should people with prediabetes do? A: At least 150 minutes of moderate aerobic activity per week (such as walking or cycling), or 75 minutes of vigorous activity, plus resistance training 2–3 times weekly.",

        "Q: Can portion control help with prediabetes? A: Yes. Eating smaller portions, practicing mindful eating, and checking food labels help prevent overeating and blood sugar spikes."



        from:https://www.medicalnewstoday.com/articles/311056#glycemic-index
        "Common in Malaysia, prediabetes affects 10.8% of adults. The risk is higher among those aged 50 and above, men, Malays, individuals who are physically inactive, and people with hypertension or a family history of diabetes.",
        "Q: How common is prediabetes in Malaysia? A: The prevalence of prediabetes is 10.8%. Higher odds are found among adults aged 50 and above, men, Malays, individuals who are physically inactive, and those with hypertension or a family history of diabetes."
    
        from: https://www.pantai.com.my/health-pulse/prediabetes-care-management
          "Q: How does the HbA1C test help in diagnosing prediabetes? A: The HbA1C test measures the average blood sugar levels over the past 2–3 months. A normal HbA1C is less than 5.7%, prediabetes is diagnosed between 5.7% and 6.4%, while diabetes is confirmed if HbA1C reaches 6.5% or higher.",

  "Q: What is the role of the fasting blood glucose test? A: This test is typically done in the morning after an eight-hour fast to check blood sugar levels. A normal result falls between 3.9 and 5.5 mmol/L, prediabetes is identified at 5.6–6.9 mmol/L, and diabetes is diagnosed at 7.0 mmol/L or higher.",

  "Q: Why is the oral glucose tolerance test important? A: It measures blood sugar before and two hours after consuming a sugary drink. A normal level is below 7.8 mmol/L, prediabetes is between 7.8 and 11.0 mmol/L, and diabetes is diagnosed if levels are 11.0 mmol/L or higher.",

  "The prediabetes diagnosed is based on the HbA1C test, where values between 5.7% and 6.4% indicate prediabetes, showing that blood sugar levels have been moderately elevated over the past few months but are not yet in the diabetes range.",

  "The prediabetes diagnosed is confirmed through the fasting blood glucose test, when results fall between 5.6 and 6.9 mmol/L, suggesting impaired fasting glucose and an increased risk of progressing to type 2 diabetes.",

  "The prediabetes diagnosed is identified through the oral glucose tolerance test, if the two-hour reading after consuming the sugary drink is between 7.8 and 11.0 mmol/L, indicating impaired glucose tolerance and higher risk of diabetes."
, "Q: How is prediabetes diagnosed? A: Prediabetes can be identified through three tests. (1) HbA1C test: measures average blood sugar over 2–3 months. Normal is < 5.7%, prediabetes is 5.7%–6.4%, and diabetes is ≥ 6.5%. (2) Fasting blood glucose test: done after an 8-hour fast. Normal is 3.9–5.5 mmol/L, prediabetes is 5.6–6.9 mmol/L, and diabetes is ≥ 7.0 mmol/L. (3) Oral glucose tolerance test: measures sugar two hours after a sugary drink. Normal is < 7.8 mmol/L, prediabetes is 7.8–11.0 mmol/L, and diabetes is ≥ 11.0 mmol/L.",
              "Summary of Prediabetes Diagnostic Tests:HbA1C Test:- Normal: < 5.7%- Prediabetes: 5.7%–6.4%- Diabetes: ≥ 6.5%Fasting Blood Glucose Test:- Normal: 3.9–5.5 mmol/L- Prediabetes: 5.6–6.9 mmol/L- Diabetes: ≥ 7.0 mmol/LOral Glucose Tolerance Test:- Normal: < 7.8 mmol/L- Prediabetes: 7.8–11.0 mmol/L- Diabetes: ≥ 11.0 mmol/L"

        from: https://www.vinmec.com/eng/blog/do-i-need-to-take-medication-if-i-have-pre-diabetes-en
  "Q: What is prediabetes and why does it happen? A: Prediabetes is a condition where blood sugar is higher than normal but not high enough for diabetes. It results from insulin resistance, when insulin cannot effectively control glucose. The body compensates by producing more insulin, but over time this may fail, leading to prediabetes.\nData: Prediabetes increases the risk of type 2 diabetes and cardiovascular disease. Risk factors include overweight, high blood pressure, and abnormal cholesterol.",

  "Prediabetes is a stage before diabetes where blood sugar is elevated due to insulin resistance. Insulin resistance worsens with age, weight gain, and lipid abnormalities. People with prediabetes are at higher risk of type 2 diabetes and cardiovascular disease, and often have high blood pressure, obesity, and unhealthy cholesterol levels.",

  "Q: How is impaired fasting glucose (IFG) and impaired glucose tolerance (IGT) diagnosed? A: IFG is diagnosed when blood sugar is elevated after fasting. IGT is diagnosed using the 75g oral glucose tolerance test (OGTT), where blood samples are taken 1 and 2 hours after drinking a sugar solution.\nData: IFG = high fasting glucose. IGT = high post-sugar glucose (OGTT: 75g sugar, test after 1h and 2h).",

  "Prediabetes may be diagnosed as impaired fasting glucose (IFG) or impaired glucose tolerance (IGT). IFG means elevated blood sugar after fasting. IGT is confirmed with a 75g oral glucose tolerance test, measuring blood glucose 1h and 2h after ingestion.",

  "Q: Can prediabetes be treated with medication? A: Yes, but only in some cases. The primary treatment is lifestyle modification (diet + exercise). Medication is considered when lifestyle changes fail, especially for patients with low HDL, high triglycerides, obesity, or family history.\nData: The only medication recognized for prediabetes management is Metformin, prescribed under endocrinologist guidance.",

  "The Ministry of Health recognizes Metformin as the only drug for prediabetes management. It is prescribed when patients fail lifestyle modification or have additional risk factors (low HDL, high triglycerides, obesity, family history of diabetes).",

  "Q: What is the recommended Metformin dosage for prediabetes? A: The effective dose is 1,000–2,000mg daily. Start low: 500mg/day in week 1, increase by 500mg/week until the desired effect. \nData: Dosage schedule → Week 1: 500mg/day. Week 2: 1,000mg/day. Week 3: 1,500mg/day. Max: 2,000mg/day.",

  "Metformin dosage for prediabetes: Start with 500mg/day in week 1. Increase gradually by 500mg each week. Usual effective range is 1,000–2,000mg/day. Prescribed only under endocrinologist supervision.",

  "Q: Why is Metformin used for prediabetes? A: Metformin improves insulin resistance, lowers blood sugar, and reduces diabetes risk. It is cost-effective, safe, and does not cause hypoglycemia.\nData: Advantages → Low cost, safe, effective in improving insulin sensitivity, does not cause hypoglycemia.",

  "Metformin (Glucophage) is widely used because it improves insulin resistance, lowers blood sugar, and reduces diabetes risk. Benefits include: low cost, safety, no risk of hypoglycemia, and potential synergy with lifestyle modification (weight loss + exercise).",

  "Q: Is prediabetes always treated with medication? A: No. Prediabetes is often reversible with lifestyle changes. Exercise (≥30 min/day) and weight loss are the most effective strategies.\nData: Lifestyle changes → Exercise 30 min/day, weight loss, healthy diet. Medication only if lifestyle fails.",

  ,"Prediabetes treatment focuses on preventing progression to diabetes. Lifestyle modification (30 minutes exercise daily, weight loss, diet changes) is first-line. Metformin can complement these changes for higher-risk patients."
    "Q: Are medications available for prediabetes? A: Yes, but they are not the first-line option. The only widely recommended drug is Metformin, prescribed when lifestyle modifications fail or for patients with additional risk factors.\nData: Metformin use → indicated if lifestyle changes ineffective, or if patient has low HDL, high triglycerides, obesity, or family history of diabetes. First-line treatment remains lifestyle modification.",

  "Metformin is the only medication currently recognized for prediabetes management. Dosage typically ranges from 1,000–2,000 mg/day, starting with 500 mg/day and increasing gradually. It is cost-effective, safe, does not cause hypoglycemia, and can complement lifestyle changes such as weight loss and ≥30 minutes of exercise per day."

,"Q: How is Metformin dosage adjusted for prediabetes patients? A: The dose starts low and is increased gradually to help the body adapt. Typically, patients begin with 500 mg/day in the first week, increase to 1,000 mg/day in the second week, and may reach up to 2,000 mg/day if needed.\nData: Week 1 → 500 mg/day; Week 2 → 1,000 mg/day; Week 3 → 1,500 mg/day; Max effective dose → 2,000 mg/day.",

  "Metformin dosage for prediabetes is titrated gradually. Patients usually start at 500 mg daily, then increase by 500 mg each week (e.g., 500 → 1,000 → 1,500 mg). The effective range is 1,000–2,000 mg/day, depending on tolerance and physician recommendation."

  from : https://www.homage.com.my/health/malaysian-food-for-diabetics/
"Q: What foods are high in fiber and good for prediabetes? A: Beans, lentils (like dhal), fruits and vegetables with edible skin such as apples, guava, and cucumbers, leafy greens, whole grains like brown rice and barley, wholemeal bread, oats, and high-fiber cereals.",

"Q: How can healthy eating prevent type 2 diabetes? A: Choose a balanced Malaysian-style diet, understand how rice and noodles affect blood glucose, eat starchy high-fibre foods like brown rice, wholemeal bread, oats, chapati, and legumes, and make sustainable dietary changes such as reducing coconut milk in curries and limiting fried foods.",

"Q: What foods should I avoid if I have prediabetes? A: Limit sugary drinks such as teh tarik, sirap bandung, and sweetened condensed milk beverages. Avoid kuih-muih, cakes, cookies, and refined carbs like white rice, white bread, and mee hoon. Limit foods high in saturated and trans fats such as deep-fried goreng pisang, keropok lekor, and fatty cuts of meat. Grapefruit and pomegranate juice may interact with medications, and high-dose supplements like ginseng, gingko, or garlic may cause low blood sugar.",

"Eating fiber-rich foods helps with satiety, digestive health, and blood sugar control. Fiber slows down glucose absorption and prevents spikes. In Malaysia, good examples include dhal curry, beans, lentils, leafy vegetables, fruits like guava, papaya, apples, vegetables with skin such as cucumber and bitter gourd, wholemeal bread, brown rice, oats, and barley water."
"Q: Can I still enjoy nasi lemak if I have prediabetes? A: Yes, but make healthier swaps. Choose brown rice or basmati rice instead of white rice, use less sambal, opt for grilled ikan bilis or chicken instead of fried, and add more cucumber and boiled egg for balance.",

"Q: What are some Malaysian drinks suitable for prediabetes? A: Choose plain water, warm water with lemon, unsweetened tea, or kopi-O kosong. Avoid sweetened condensed milk, sugary syrups, bubble tea, and packet drinks high in sugar.",

"Q: What are healthier Malaysian snacks for prediabetes? A: Try boiled corn, steamed kacang kuda (chickpeas), roasted groundnuts, fresh fruits like papaya or guava, and cucur sayur made with less oil, instead of kuih-muih high in sugar and coconut milk.",

"Q: How important is portion control in prediabetes? A: Very important. Use the Malaysian healthy plate concept: half the plate vegetables, a quarter protein (fish, chicken, tofu, dhal), and a quarter whole grains or brown rice. This helps manage blood sugar while still enjoying local foods."
  

    """



