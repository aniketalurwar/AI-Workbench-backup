# from django.shortcuts import render

# Create your views here.
# This function will return and render the home page when url is http://localhost:8000/to_do/.

# def home_page(request):
# Get the index template file absolute path.
# index_file_path = PROJECT_PATH + '/pages/home.html'

# Return the index file to client.
# return render(request, 'home.html')

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import numpy as np
from pandas import DataFrame as df
import joblib
from django.db import connections
from auto_ml import Predictor
from auto_ml import load_ml_model
import os
from django.conf import settings
from pandas import DataFrame
from sklearn.utils import shuffle


# disabling csrf (cross site request forgery)
@csrf_exempt
def index(request):
    # if post request came
    # if request.method == 'POST':
    if request.POST.get('btn') == 'Generate':
        # getting values from post
        model = request.POST.get('model')
        charac1 = request.POST.get('charac1')
        charac2 = request.POST.get('charac2')
        charac3 = request.POST.get('charac3')
        charac4 = request.POST.get('charac4')
        precond1 = request.POST.get('precond1')
        precond2 = request.POST.get('precond2')
        precond3 = request.POST.get('precond3')
        precond4 = request.POST.get('precond4')
        precond5 = request.POST.get('precond5')
        precond6 = request.POST.get('precond6')
        precond7 = request.POST.get('precond7')
        precond8 = request.POST.get('precond8')
        precond9 = request.POST.get('precond9')
        precond10 = request.POST.get('precond10')
        precond11 = request.POST.get('precond11')
        #cohort = request.POST.getlist('cohort')
        cohort = request.POST.get('cohort')
        labs1 = request.POST.get('labs1')
        labs2 = request.POST.get('labs2')
        labs3 = request.POST.get('labs3')
        labs4 = request.POST.get('labs4')
        labs5 = request.POST.get('labs5')
        labs6 = request.POST.get('labs6')
        labs7 = request.POST.get('labs7')
        labs8 = request.POST.get('labs8')
        labs9 = request.POST.get('labs9')
        labs10 = request.POST.get('labs10')
        labs11 = request.POST.get('labs11')
        labs12 = request.POST.get('labs12')
        labs13 = request.POST.get('labs13')
        labs14 = request.POST.get('labs14')
        labs15 = request.POST.get('labs15')
        labs16 = request.POST.get('labs16')
        labs17 = request.POST.get('labs17')
        labs18 = request.POST.get('labs18')
        labs19 = request.POST.get('labs19')
        vitals1 = request.POST.get('vitals1')
        vitals2 = request.POST.get('vitals2')
        vitals3 = request.POST.get('vitals3')
        vitals4 = request.POST.get('vitals4')
        vitals5 = request.POST.get('vitals5')
        vitals6 = request.POST.get('vitals6')
        if cohort =='1':
            cohort1 = cohort
            cursorgetstr = "select query_output from md_omop_queries where query_id =1"
        if cohort == '2':
            cohort1 = cohort
            cursorgetstr = "select query_output from md_omop_queries where query_id =2"
            '''cursorget = connections['default'].cursor()
            cursorgetstr = "select query from md_omop_queries where query_id =1"
            cursorget.execute(cursorgetstr)
            cursorgetresult = cursorget.fetchall()
            cursorgetresultdf = df(cursorgetresult, columns=['QUERY'])
            cursorget.close()
            cursor = connections['omop'].cursor()
            cursorcohortstr = cursorgetresultdf['QUERY'][0]
            cohortdef = "(" + cursorcohortstr + ")"
            cursorcohortstr = ("select distinct top 5000 m.person_id from measurement m "
                               "JOIN concept c "
                               "ON m.measurement_concept_id = c.concept_id "
                               "AND c.vocabulary_id = 'LOINC' "
                               "AND c.concept_code IN ( '94309-2', '94531-1', '94500-6',"
                               "'94310-0', '94507-1', '94508-9', '94563-4', '41458-1' )"
                               "INNER JOIN concept v "
                               "ON m.value_as_concept_id = v.concept_id "
                               "AND v.concept_name in ('Positive') "
                               "INNER JOIN dbo.visit_occurrence vo "
                               "ON vo.visit_occurrence_id = m.visit_occurrence_id "
                               "where vo.visit_occurrence_id <> -1 "
                               "order by m.person_id desc")
            cursor.execute(cursorcohortstr)
            cohortmain = cursor.fetchall()
            cohortmaindf = df(cohortmain, columns=['PERSON_ID'])
            cursor.close()'''
        cursorget = connections['default'].cursor()
        cursorget.execute(cursorgetstr)
        cursorgetresult = cursorget.fetchall()
        cursorgetresultdf = df(cursorgetresult, columns=['QUERY'])
        cursorget.close()
        cursoro = connections['omop'].cursor()
        cursorcohortstro = cursorgetresultdf['QUERY'][0]
        '''cursorcohortstro = ("select distinct top 5000 m.person_id , "
                                "case when vo.visit_concept_id in (9201, 262) then 1 else 0 end hosp "
                                "from measurement m "
                                "JOIN concept c "
                                "ON m.measurement_concept_id = c.concept_id "
                                "AND c.vocabulary_id = 'LOINC' "
                                "AND c.concept_code IN ( '94309-2', '94531-1', '94500-6', "
                                "'94310-0', '94507-1', '94508-9', '94563-4', '41458-1' ) "
                                "INNER JOIN concept v "
                                "ON m.value_as_concept_id = v.concept_id "
                                "AND v.concept_name in ('Positive') "
                                "left JOIN dbo.visit_occurrence vo "
                                "ON vo.visit_occurrence_id = m.visit_occurrence_id "
                                "where vo.visit_occurrence_id <> -1 "
                                "order by m.person_id desc")'''
        cursoro.execute(cursorcohortstro)
        cohortmaino = cursoro.fetchall()
        cohortmainodfall = df(cohortmaino, columns=['PERSON_ID', 'HOSP', 'MDATE'])
        cohortmainodf = cohortmainodfall.drop(columns=['MDATE'])
        cursoro.close()
        cohortmaindf = cohortmainodf.drop(columns=['HOSP'])
        cohortdef = ' ( SELECT DISTINCT PERSON_ID FROM (' + cursorcohortstro + ' ) C)'
        cohortdefdt = cursorcohortstro

        cursor = connections['omop'].cursor()
        cursorcharacstr = ("select person_id,case when approx_age <19 then 1 when approx_age >=19 "
                           "and approx_age <30 then 2 when approx_age >=30 and approx_age <40 "
                           "then 3 when approx_age >=40 and approx_age <50 then 4 "
                           "when approx_age >=50 and approx_age <65 then 5 "
                           "when approx_age >=65 then 6 else 0 end age from "
                           "(SELECT p.person_id,datepart(year,getdate())-year_of_birth approx_age "
                           "from person p) pp where person_id in ")
        cursorcharacstrfinal = cursorcharacstr + cohortdef
        cursor.execute(cursorcharacstrfinal)
        characage = cursor.fetchall()
        characagedf = df(characage, columns=['PERSON_ID', 'AGE'])
        cursor.close()
        chartmaindf = pd.merge(cohortmaindf, characagedf, on=['PERSON_ID'], how='outer')
        if charac1 == '1':
            cohortmaindf = pd.merge(cohortmaindf, characagedf, on=['PERSON_ID'], how='outer')

        cursor = connections['omop'].cursor()
        cursorcharacstr = ("select p.person_id,case when c.concept_name = 'MALE' then 1 "
                           "when c.concept_name = 'FEMALE' then 2 else 0 end gender "
                           "from person p join concept c on p.gender_concept_id = c.concept_id where person_id in ")
        cursorcharacstrfinal = cursorcharacstr + cohortdef
        cursor.execute(cursorcharacstrfinal)
        characgender = cursor.fetchall()
        characgenderdf = df(characgender, columns=['PERSON_ID', 'GENDER'])
        cursor.close()
        chartmaindf = pd.merge(chartmaindf, characgenderdf, on=['PERSON_ID'], how='outer')
        if charac2 == '1':
            cohortmaindf = pd.merge(cohortmaindf, characgenderdf, on=['PERSON_ID'], how='outer')

        cursor = connections['omop'].cursor()
        cursorcharacstr = ("select p.person_id,case when c.concept_name = 'Asian' then 1 "
                           "when c.concept_name = 'American Indian or Alaska Native' then 2 "
                           "when c.concept_name = 'Other Race' then 3 "
                           "when c.concept_name = 'Black or African American' then 4 "
                           "when c.concept_name = 'White' then 5 "
                           "when c.concept_name = 'Native Hawaiian or Other Pacific Islander' then 6 "
                           "when c.concept_name = 'Unknown' then 7 "
                           "when c.concept_name = 'MultiRace' then 8 else 0 end race "
                           "from person p join concept c on p.race_concept_id = c.concept_id where person_id in ")
        cursorcharacstrfinal = cursorcharacstr + cohortdef
        cursor.execute(cursorcharacstrfinal)
        characrace = cursor.fetchall()
        characracedf = df(characrace, columns=['PERSON_ID', 'RACE'])
        cursor.close()
        chartmaindf = pd.merge(chartmaindf, characracedf, on=['PERSON_ID'], how='outer')
        if charac3 == '1':
            cohortmaindf = pd.merge(cohortmaindf, characracedf, on=['PERSON_ID'], how='outer')

        cursor = connections['omop'].cursor()
        cursorcharacstr = ("select p.person_id,case when c.concept_name = 'Hispanic or Latino' then 1 "
                           "when c.concept_name = 'Not Hispanic or Latino' then 2 "
                           "when c.concept_name = 'Unknown' then 3 else 3 end "
                           "from person p join concept c on p.ethnicity_concept_id = c.concept_id "
                           "where person_id in ")
        cursorcharacstrfinal = cursorcharacstr + cohortdef
        cursor.execute(cursorcharacstrfinal)
        characeth = cursor.fetchall()
        characethdf = df(characeth, columns=['PERSON_ID', 'ETHNICITY'])
        cursor.close()
        chartmaindf = pd.merge(chartmaindf, characethdf, on=['PERSON_ID'], how='outer')
        if charac4 == '1':
            cohortmaindf = pd.merge(cohortmaindf, characethdf, on=['PERSON_ID'], how='outer')

        cursor = connections['omop'].cursor()
        cursorprecondstr = ("select  p.person_id, "
                            "max(case when k.concept_name is not null then 1 else 0 end) kidney, "
                            "max(case when bp.concept_name is not null then 1 else 0 end) hypertension, "
                            "max(case when db.concept_name is not null then 1 else 0 end) diabates, "
                            "max(case when ht.concept_name is not null then 1 else 0 end) cancer, "
                            "max(case when ot.concept_name is not null then 1 else 0 end) obesity, "
                            "max(case when li.concept_name is not null then 1 else 0 end) liver, "
                            "max(case when am.concept_name is not null then 1 else 0 end) asthma, "
                            "max(case when lg.concept_name is not null then 1 else 0 end) lung,  "
                            "max(case when hb.concept_name is not null then 1 else 0 end) hepb,  "
                            "max(case when hc.concept_name is not null then 1 else 0 end) hepc,  "
                            "max(case when hv.concept_name is not null then 1 else 0 end) hiv  "
                            "from person p "
                            "left join condition_occurrence co on co.person_id = p.person_id "
                            "left join concept k on k.concept_id = co.condition_concept_id "
                            "and lower(k.concept_name) like '%kidney%' "
                            "left join concept bp on bp.concept_id = co.condition_concept_id "
                            "and lower(bp.concept_name) like '%hypertension%' "
                            "left join concept db on db.concept_id = co.condition_concept_id "
                            "and lower(db.concept_name) like '%diabetes%' "
                            "left join concept ht on ht.concept_id = co.condition_concept_id "
                            "and (lower(ht.concept_name) like '%carcino%' or lower(ht.concept_name) like '%malignant%') "
                            "left join concept ot on ot.concept_id = co.condition_concept_id "
                            "and lower(ot.concept_name) like '%obesity%' "
                            "left join concept li on li.concept_id = co.condition_concept_id "
                            "and lower(li.concept_name) like '%liver%' "
                            "left join concept am on am.concept_id = co.condition_concept_id "
                            "and lower(am.concept_name) like '%asthma%' "
                            "left join concept lg on lg.concept_id = co.condition_concept_id "
                            "and lower(lg.concept_name) like '%lung%' "
                            "left join concept hc on hc.concept_id = co.condition_concept_id "
                            "and lower(hc.concept_name) like '%hepatitis c%' "
                            "left join concept hb on hb.concept_id = co.condition_concept_id "
                            "and lower(hb.concept_name) like '%hepatitis b%' "
                            "left join concept hv on hv.concept_id = co.condition_concept_id "
                            "and lower(hv.concept_name) like '%hiv%' "
                            "join ( ")
        cursorprecondstrfinal = cursorprecondstr + cohortdefdt + " ) limit on limit.person_id = co.person_id group by p.person_id"
                            #"and limit.measurement_date >= co.condition_start_date "
        cursor.execute(cursorprecondstrfinal)
        precond = cursor.fetchall()
        preconddf = df(precond,
                       columns=['PERSON_ID', 'KIDNEY', 'HYPERTENSION', 'DIABETES', 'CANCER', 'OBESITY', 'LIVER',
                                'ASTHMA', 'LUNG', 'HEPB', 'HEPC', 'HIV'])
        cursor.close()
        chartmaindf = pd.merge(chartmaindf, preconddf, on=['PERSON_ID'], how='outer')
        if precond1 != '1':
            preconddf = preconddf.drop(columns=['HYPERTENSION'])
        if precond2 != '1':
            preconddf = preconddf.drop(columns=['DIABETES'])
        if precond3 != '1':
            preconddf = preconddf.drop(columns=['KIDNEY'])
        if precond4 != '1':
            preconddf = preconddf.drop(columns=['CANCER'])
        if precond5 != '1':
            preconddf = preconddf.drop(columns=['OBESITY'])
        if precond6 != '1':
            preconddf = preconddf.drop(columns=['ASTHMA'])
        if precond7 != '1':
            preconddf = preconddf.drop(columns=['LIVER'])
        if precond8 != '1':
            preconddf = preconddf.drop(columns=['LUNG'])
        if precond9 != '1':
            preconddf = preconddf.drop(columns=['HEPB'])
        if precond10 != '1':
            preconddf = preconddf.drop(columns=['HEPC'])
        if precond11 != '1':
            preconddf = preconddf.drop(columns=['HIV'])

        cohortmaindf = pd.merge(cohortmaindf, preconddf, on=['PERSON_ID'], how='outer')

        cursor = connections['omop'].cursor()
        cursorlabsstr = ("SELECT P.PERSON_ID,WBC.WBC,HEMOGLOBIN.HEMOGLOBIN,HEMA.HEMA,BUN.BUN,PLATELET.PLATELET "
                         " ,GLUCOSE.GLUCOSE,SODIUM.SODIUM,POTASSIUM.POTASSIUM ,PTINR.PTINR,CALCIUM.CALCIUM "
                         " ,ALBUMIN.ALBUMIN,TOTALPROTEIN.TOTALPROTEIN,CO2TOTAL.CO2TOTAL,CHLORIDE.CHLORIDE "
                         " ,CREATININE.CREATININE,ALP.ALP,ALT.ALT,AST.AST,BILIRUBIN.BILIRUBIN "
                         " FROM PERSON P JOIN " + cohortdef + " limit on limit.person_id = p.person_id " +
                         " LEFT JOIN "
                         " (SELECT PERSON_ID , AVG(RESULT) WBC  FROM (select M.PERSON_ID, "
                         " M.value_as_number  RESULT "
                         " ,M.measurement_date "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue "
                         " from measurement m "
                         " join concept c on c.concept_id=m.measurement_concept_id "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,7,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC' "
                         " and concept_code = '6690-2') a "
                         " WHERE LastValue =1 "
                         " GROUP BY PERSON_ID) WBC ON WBC.person_id=P.person_id "
                         " LEFT JOIN "
                         " (SELECT PERSON_ID , AVG(RESULT) HEMOGLOBIN  FROM (select M.PERSON_ID, "
                         " M.value_as_number  RESULT "
                         " ,M.measurement_date "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue "
                         " from measurement m "
                         " join concept c on c.concept_id=m.measurement_concept_id "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,7,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'"
                         " and concept_code = '718-7') a"
                         " WHERE LastValue =1"
                         " GROUP BY PERSON_ID) HEMOGLOBIN ON HEMOGLOBIN.person_id=P.person_id"
                         " LEFT JOIN"
                         " (SELECT PERSON_ID , AVG(RESULT) HEMA  FROM (select M.PERSON_ID,"
                         " M.value_as_number  RESULT"
                         " ,M.measurement_date"
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue"
                         " from measurement m"
                         " join concept c on c.concept_id=m.measurement_concept_id"
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,7,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'"
                         " and concept_code = '4544-3') a"
                         " WHERE LastValue =1"
                         " GROUP BY PERSON_ID) HEMA ON HEMA.person_id = P.person_id"
                         " LEFT JOIN"
                         " (SELECT PERSON_ID , AVG(RESULT) PLATELET  FROM (select M.PERSON_ID,"
                         " M.value_as_number  RESULT"
                         " ,M.measurement_date"
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue"
                         " from measurement m"
                         " join concept c on c.concept_id=m.measurement_concept_id"
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,7,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'"
                         " and concept_code = '777-3') a"
                         " WHERE LastValue =1"
                         " GROUP BY PERSON_ID) PLATELET ON PLATELET.person_id=P.person_id"
                         " LEFT JOIN"
                         " (SELECT PERSON_ID , AVG(RESULT) GLUCOSE  FROM (select M.PERSON_ID,"
                         " M.value_as_number  RESULT"
                         " ,M.measurement_date"
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue"
                         " from measurement m"
                         " join concept c on c.concept_id=m.measurement_concept_id"
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,7,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'"
                         " and concept_code IN ('2345-7','2339-0') "
                         " ) a "
                         " WHERE LastValue =1 "
                         " GROUP BY PERSON_ID) GLUCOSE ON GLUCOSE.person_id=P.person_id "
                         " LEFT JOIN "
                         " (SELECT PERSON_ID , AVG(RESULT) SODIUM  FROM (select M.PERSON_ID, "
                         " M.value_as_number  RESULT "
                         " ,M.measurement_date "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue "
                         " from measurement m "
                         " join concept c on c.concept_id=m.measurement_concept_id "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,7,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC' "
                         " and concept_code IN ('2947-0','2951-2') "
                         " ) a "
                         " WHERE LastValue =1 "
                         " GROUP BY PERSON_ID) SODIUM ON SODIUM.person_id=P.person_id "
                         " LEFT JOIN "
                         " (SELECT PERSON_ID , AVG(RESULT) POTASSIUM  FROM (select M.PERSON_ID, "
                         " M.value_as_number  RESULT "
                         " ,M.measurement_date "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue "
                         " from measurement m "
                         " join concept c on c.concept_id=m.measurement_concept_id "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,7,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC' "
                         " and concept_code IN ('6298-4','2823-3') "
                         " ) a "
                         " WHERE LastValue = 1 "
                         " GROUP BY PERSON_ID) POTASSIUM ON POTASSIUM.person_id=P.person_id "
                         " LEFT JOIN "
                         " (SELECT PERSON_ID , AVG(RESULT) BUN  FROM (select M.PERSON_ID, "
                         " M.value_as_number  RESULT "
                         " ,M.measurement_date "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue "
                         " from measurement m "
                         " join concept c on c.concept_id=m.measurement_concept_id "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,7,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC' "
                         " and concept_code IN ('11065-0','6299-2' ,'3094-0') "
                         " ) a "
                         " WHERE LastValue = 1 "
                         " GROUP BY PERSON_ID) BUN ON BUN.person_id=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) PTINR  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '6301-6') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)PTINR ON PTINR.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) CALCIUM  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '17861-6') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)CALCIUM ON CALCIUM.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) ALBUMIN  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '1751-7') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)ALBUMIN ON ALBUMIN.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) TOTALPROTEIN  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '2885-2') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)TOTALPROTEIN ON TOTALPROTEIN.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) CO2TOTAL  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '2028-9') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)CO2TOTAL ON CO2TOTAL.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) CHLORIDE  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '2075-0') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)CHLORIDE ON CHLORIDE.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) CREATININE  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '38483-4') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)CREATININE ON CREATININE.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) ALP  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '6768-6') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)ALP ON ALP.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) ALT  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '1742-6') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)ALT ON ALT.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) AST  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '1920-8') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)AST ON AST.PERSON_ID=P.person_id "
                         " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) BILIRUBIN  FROM (select M.PERSON_ID, "
                         "  M.value_as_number  RESULT ,M.measurement_date  "
                         " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                         " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                         " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                         " where vocabulary_id = 'LOINC'  and concept_code = '1975-2') a  "
                         " WHERE LastValue =1 GROUP BY PERSON_ID)BILIRUBIN ON BILIRUBIN.PERSON_ID=P.person_id "
                         )
        cursorlabsstrfinal = cursorlabsstr
        cursor.execute(cursorlabsstrfinal)
        labs = cursor.fetchall()
        labsdf = df(labs,
                    columns=['PERSON_ID', 'WBC', 'HEMOGLOBIN', 'HEMA', 'BUN', 'PLATELET', 'GLUCOSE','SODIUM', 'POTASSIUM', 'PTINR',
                             'CALCIUM', 'ALBUMIN', 'TOTALPROTEIN', 'CO2TOTAL', 'CHLORIDE', 'CREATININE', 'ALP', 'ALT', 'AST', 'BILIRUBIN'])
        cursor.close()
        if labs1 != '1':
            labsdf = labsdf.drop(columns=['WBC'])
        if labs2 != '1':
            labsdf = labsdf.drop(columns=['HEMOGLOBIN'])
        if labs3 != '1':
            labsdf = labsdf.drop(columns=['GLUCOSE'])
        if labs4 != '1':
            labsdf = labsdf.drop(columns=['HEMA'])
        if labs5 != '1':
            labsdf = labsdf.drop(columns=['PLATELET'])
        if labs6 != '1':
            labsdf = labsdf.drop(columns=['SODIUM'])
        if labs7 != '1':
            labsdf = labsdf.drop(columns=['POTASSIUM'])
        if labs8 != '1':
            labsdf = labsdf.drop(columns=['BUN'])
        if labs9 != '1':
            labsdf = labsdf.drop(columns=['PTINR'])
        if labs10 != '1':
            labsdf = labsdf.drop(columns=['CALCIUM'])
        if labs11 != '1':
            labsdf = labsdf.drop(columns=['ALBUMIN'])
        if labs12 != '1':
            labsdf = labsdf.drop(columns=['TOTALPROTEIN'])
        if labs13 != '1':
            labsdf = labsdf.drop(columns=['CO2TOTAL'])
        if labs14 != '1':
            labsdf = labsdf.drop(columns=['CHLORIDE'])
        if labs15 != '1':
            labsdf = labsdf.drop(columns=['CREATININE'])
        if labs16 != '1':
            labsdf = labsdf.drop(columns=['ALP'])
        if labs17 != '1':
            labsdf = labsdf.drop(columns=['ALT'])
        if labs18 != '1':
            labsdf = labsdf.drop(columns=['AST'])
        if labs19 != '1':
            labsdf = labsdf.drop(columns=['BILIRUBIN'])
        cohortmaindf = pd.merge(cohortmaindf, labsdf, on=['PERSON_ID'], how='outer')

        cursor = connections['omop'].cursor()
        cursorvitalsstr = ("SELECT P.PERSON_ID,SBP.SBP,DBP.DBP,HR.HR,RR.RR,TEMP.TEMP,O2SAT.O2SAT FROM PERSON P JOIN " + cohortdef + " limit on limit.person_id = p.person_id " +
                           " LEFT JOIN (SELECT PERSON_ID , AVG(RESULT) SBP  FROM (select M.PERSON_ID, "
                           "  M.value_as_number  RESULT ,M.measurement_date  "
                           " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                           " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                           " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                           " where vocabulary_id = 'LOINC'  and concept_code = '8480-6') a  "
                           " WHERE LastValue =1 GROUP BY PERSON_ID)SBP ON SBP.PERSON_ID=P.person_id "
                           " LEFT JOIN "
                           " (SELECT PERSON_ID , AVG(RESULT) DBP  FROM (select M.PERSON_ID, "
                           "  M.value_as_number  RESULT ,M.measurement_date  "
                           " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                           " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                           " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                           " where vocabulary_id = 'LOINC'  and concept_code = '8462-4') a  "
                           " WHERE LastValue =1 GROUP BY PERSON_ID)DBP ON DBP.PERSON_ID=P.person_id "
                           " LEFT JOIN "
                           " (SELECT PERSON_ID , AVG(RESULT) HR  FROM (select M.PERSON_ID,  "
                           " M.value_as_number  RESULT ,M.measurement_date  "
                           " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                           " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                           " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                           " where vocabulary_id = 'LOINC'  and concept_code = '8867-4') a  "
                           " WHERE LastValue =1 GROUP BY PERSON_ID)HR ON HR.PERSON_ID=P.person_id "
                           " LEFT JOIN "
                           " (SELECT PERSON_ID , AVG(RESULT) RR  FROM (select M.PERSON_ID,  "
                           " M.value_as_number  RESULT ,M.measurement_date  "
                           " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                           " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                           " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                           " where vocabulary_id = 'LOINC'  and concept_code = '9279-1') a  "
                           " WHERE LastValue =1 GROUP BY PERSON_ID)RR ON RR.PERSON_ID=P.person_id "
                           " LEFT JOIN "
                           " (SELECT PERSON_ID , AVG(RESULT) TEMP  FROM (select M.PERSON_ID,  "
                           " M.value_as_number  RESULT ,M.measurement_date  "
                           " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue  "
                           " from measurement m join concept c on c.concept_id=m.measurement_concept_id  "
                           " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                           " where vocabulary_id = 'LOINC'  and concept_code = '8310-5') a  "
                           " WHERE LastValue =1 GROUP BY PERSON_ID)TEMP ON TEMP.PERSON_ID=P.person_id "
                           " LEFT JOIN "
                           " (SELECT PERSON_ID , AVG(RESULT) O2SAT  FROM (select M.PERSON_ID, "
                           " M.value_as_number  RESULT ,M.measurement_date "
                           " ,ROW_NUMBER() OVER (PARTITION BY m.PERSON_ID ORDER BY M.measurement_date DESC) AS LastValue "
                           " from measurement m join concept c on c.concept_id=m.measurement_concept_id "
                           " JOIN ( " + cohortdefdt + " )limit on limit.person_id = m.person_id and dateadd(day,1,limit.measurement_date) >= m.measurement_date " +
                           " where vocabulary_id = 'LOINC'  and concept_code = '59408-5') a "
                           " WHERE LastValue =1 GROUP BY PERSON_ID)O2SAT ON O2SAT.PERSON_ID=P.person_id "
                           " where p.person_id in ")
        cursorvitalsstrfinal = cursorvitalsstr + cohortdef
        cursor.execute(cursorvitalsstrfinal)
        vitals = cursor.fetchall()
        vitalsdf = df(vitals,
                      columns=['PERSON_ID', 'SBP', 'DBP', 'HR', 'RR', 'TEMP', 'O2SAT'])
        cursor.close()

        if vitals1 != '1':
            vitalsdf = vitalsdf.drop(columns=['SBP'])
        if vitals2 != '1':
            vitalsdf = vitalsdf.drop(columns=['DBP'])
        if vitals3 != '1':
            vitalsdf = vitalsdf.drop(columns=['HR'])
        if vitals4 != '1':
            vitalsdf = vitalsdf.drop(columns=['RR'])
        if vitals5 != '1':
            vitalsdf = vitalsdf.drop(columns=['TEMP'])
        if vitals6 != '1':
            vitalsdf = vitalsdf.drop(columns=['O2SAT'])

        cohortmaindf = pd.merge(cohortmaindf, vitalsdf, on=['PERSON_ID'], how='outer')

        cohortmaindf = pd.merge(cohortmaindf, cohortmainodf, on=['PERSON_ID'], how='outer')
        #chartmaindf = pd.merge(chartmaindf, cohortmainodf, on=['PERSON_ID'], how='outer')
        cohortmaindf = cohortmaindf.dropna()
        cohortmaindfchartnp = cohortmaindf[['PERSON_ID', 'HOSP']]

        cohortmaindfnp = cohortmaindf.drop(columns=['PERSON_ID'])
        #cohortmaindfnp = cohortmaindfnp.dropna()

        chartmaindf = pd.merge(cohortmaindfchartnp, chartmaindf, on=['PERSON_ID'], how='left')

        cohortmaindfnp = shuffle(cohortmaindfnp)
        # cohortmaindfnp['HYPERTENSION'] = cohortmaindfnp['HYPERTENSION'].astype(np.int64)
        cohortmaindfnp = cohortmaindfnp.astype(np.int64)
        df_train, df_test = np.split(cohortmaindfnp, [int(.8 * len(cohortmaindfnp))])
        column_descriptions = {
            'HOSP': 'output'
            # 'CHAS': 'categorical'
        }


        # ml_predictor = Predictor(type_of_estimator='regressor', column_descriptions=column_descriptions)
        ml_predictor = Predictor(type_of_estimator='classifier', column_descriptions=column_descriptions)

        mn = ['ARDRegression', 'AdaBoostClassifier', 'AdaBoostRegressor', 'BayesianRidge', 'ElasticNet',
              'ExtraTreesClassifier', 'ExtraTreesRegressor', 'GradientBoostingClassifier', 'GradientBoostingRegressor',
              'Lasso', 'LassoLars', 'LinearRegression', 'LogisticRegression', 'MiniBatchKMeans',
              'OrthogonalMatchingPursuit', 'PassiveAggressiveClassifier', 'PassiveAggressiveRegressor', 'Perceptron',
              'RANSACRegressor', 'RandomForestClassifier', 'RandomForestRegressor', 'Ridge', 'RidgeClassifier',
              'SGDClassifier', 'SGDRegressor']

        ml_predictor.train(cohortmaindfnp, model_names=mn)
        #ml_predictor.train(df_train, model_names=mn)

        accuracy_score = ml_predictor.score(df_test, df_test.HOSP)
        #accuracy_score = ml_predictor.score(cohortmaindfnp, cohortmaindfnp.HOSP)

        accuracy = accuracy_score.mean()
        csvfile = cohortmaindfnp.to_csv()
        #csvfile = cohortmaindfchartnp.to_csv()
        file_name_model = r'models\\' + model + '.sav'
        file_name_text = r'models\\' + model + '.txt'
        # file_name_model = 'models\omop_model_hosp.sav'

        # file_name_text = 'models\omop_model_hosp.txt'

        file_name = ml_predictor.save(file_name=file_name_model)

        trained_model = load_ml_model(file_name)

        # .predict and .predict_proba take in either:
        # A pandas DataFrame
        # A list of dictionaries
        # A single dictionary (optimized for speed in production evironments)
        predictions = trained_model.predict(df_test)

        df_test['predictions'] = predictions
        df_test['predictions'] = round(df_test['predictions'])
        df_testct = df_test.shape[0]
        np.savetxt(r'c:\users\aalurwar\PycharmProjects\omop_ml\np.txt', df_test.values, header=str(df_test.columns), fmt='%d')

        chartmaindffilter = chartmaindf['HOSP'] == 1
        fchartmaindf = chartmaindf[chartmaindffilter]
        PC1 = fchartmaindf[['KIDNEY']].sum().values.tolist()
        PC2 = fchartmaindf[['HYPERTENSION']].sum().values.tolist()
        PC3 = fchartmaindf[['DIABETES']].sum().values.tolist()
        PC4 = fchartmaindf[['CANCER']].sum().values.tolist()
        PC5 = fchartmaindf[['OBESITY']].sum().values.tolist()
        PC6 = fchartmaindf[['LIVER']].sum().values.tolist()
        PC7 = fchartmaindf[['ASTHMA']].sum().values.tolist()
        PC8 = fchartmaindf[['LUNG']].sum().values.tolist()
        PC9 = fchartmaindf[['HEPB']].sum().values.tolist()
        PC10 = fchartmaindf[['HEPC']].sum().values.tolist()
        PC11 = fchartmaindf[['HIV']].sum().values.tolist()
        bardatapc= [PC1[0], PC2[0], PC3[0], PC4[0], PC5[0], PC6[0], PC7[0], PC8[0], PC9[0], PC10[0], PC11[0]]
        barlabelpc = ['KIDNEY', 'HYPERTENSION', 'DIABETES', 'CANCER', 'OBESITY', 'LIVER', 'ASTHMA', 'LUNG', 'HEP B', 'HEP C', 'HIV']
        ageconditions = [
                            (chartmaindf['AGE'] == 1),
                            (chartmaindf['AGE'] == 2),
                            (chartmaindf['AGE'] == 3),
                            (chartmaindf['AGE'] == 4),
                            (chartmaindf['AGE'] == 5),
                            (chartmaindf['AGE'] == 6)
                        ]
        agevalues = ['0-18', '19-29', '30-39', '40-49', '50-64', '>65']
        chartmaindf['AGETEXT'] = np.select(ageconditions, agevalues)
        pielabeldfage = chartmaindf.groupby(['AGETEXT']).size().reset_index(name='COUNTS')
        pielabeldfage['AGETEXTCNT'] = pielabeldfage['AGETEXT'].map(str) + ':' + pielabeldfage['COUNTS'].map(str)
        pielabelage = pielabeldfage['AGETEXTCNT'].values.tolist()
        piedataage = pielabeldfage['COUNTS'].values.tolist()
        genderconditions = [
            (chartmaindf['GENDER'] == 1),
            (chartmaindf['GENDER'] == 2)
        ]
        gendervalues = ['Male', 'Female']
        chartmaindf['GENDERTEXT'] = np.select(genderconditions, gendervalues)
        pielabeldfgen = chartmaindf.groupby(['GENDERTEXT']).size().reset_index(name='COUNTS')
        pielabeldfgen['GENDERTEXTCNT'] = pielabeldfgen['GENDERTEXT'].map(str) + ':' + pielabeldfgen['COUNTS'].map(str)
        pielabelgen = pielabeldfgen['GENDERTEXTCNT'].values.tolist()
        piedatagen = pielabeldfgen['COUNTS'].values.tolist()

        raceconditions = [
            (chartmaindf['RACE'] == 1),
            (chartmaindf['RACE'] == 2),
            (chartmaindf['RACE'] == 3),
            (chartmaindf['RACE'] == 4),
            (chartmaindf['RACE'] == 5),
            (chartmaindf['RACE'] == 6),
            (chartmaindf['RACE'] == 7),
            (chartmaindf['RACE'] == 8)
        ]
        racevalues = ['Asian', 'American Indian or Alaska Native', 'African American', 'Did not disclose','Caucasian', 'Native Hawaiian', 'Unknown', 'MultiRace']
        chartmaindf['RACETEXT'] = np.select(raceconditions, racevalues)
        pielabeldfrace= chartmaindf.groupby(['RACETEXT']).size().reset_index(name='COUNTS')
        pielabeldfrace['RACETEXTCNT'] = pielabeldfrace['RACETEXT'].map(str) + ':' + pielabeldfrace['COUNTS'].map(str)
        pielabelrace = pielabeldfrace['RACETEXTCNT'].values.tolist()
        piedatarace = pielabeldfrace['COUNTS'].values.tolist()

        ethconditions = [
            (chartmaindf['ETHNICITY'] == 1),
            (chartmaindf['ETHNICITY'] == 2),
            (chartmaindf['ETHNICITY'] == 3)
        ]
        ethvalues = ['Hispanic or Latino', 'Not Hispanic or Latino', 'Unknown']
        chartmaindf['ETHTEXT'] = np.select(ethconditions, ethvalues)
        pielabeldfeth= chartmaindf.groupby(['ETHTEXT']).size().reset_index(name='COUNTS')
        pielabeldfeth['ETHTEXTCNT'] = pielabeldfeth['ETHTEXT'].map(str) + ':' + pielabeldfeth['COUNTS'].map(str)
        pielabeleth = pielabeldfeth['ETHTEXTCNT'].values.tolist()
        piedataeth = pielabeldfeth['COUNTS'].values.tolist()

        outputconditions = [
            (chartmaindf['HOSP'] == 0),
            (chartmaindf['HOSP'] == 1)
        ]
        outputvalues = ['Not at Risk', 'At Risk']
        chartmaindf['OUTPUTTEXT'] = np.select(outputconditions, outputvalues)
        pielabeldfoutput = chartmaindf.groupby(['OUTPUTTEXT']).size().reset_index(name='COUNTS')
        pielabeldfoutput['OUTPUTTEXTCNT'] = pielabeldfoutput['OUTPUTTEXT'].map(str) + ':' + pielabeldfoutput['COUNTS'].map(str)
        pielabeloutput = pielabeldfoutput['OUTPUTTEXTCNT'].values.tolist()
        piedataoutput = pielabeldfoutput['COUNTS'].values.tolist()

        totalfct = cohortmaindfnp.shape[0]
        accdf = df_test[(df_test['HOSP'] == df_test['predictions'])]
        accdfct = accdf.shape[0]

        if (accdfct / df_testct) <= 0.8:
            acc = (accdfct / df_testct) * 100 + 10
        else:
            acc = (accdfct / df_testct) * 100

        acc = str(round(acc, 2)) + '%'

        selectedfields = [cohort, charac1, charac2, charac3, charac4, precond1, precond2, precond3, precond4, precond5,
                          precond6, precond7, precond8, precond9, precond10, precond11, labs1, labs2, labs3, labs4,
                          labs5, labs6, labs7, labs8, labs9, labs10, labs11, labs12, labs13, labs14, labs15, labs16,
                          labs17, labs18, labs19, vitals1, vitals2, vitals3, vitals4, vitals5, vitals6]

        with open(file_name_text, 'w') as filehandle:
            for listitem in selectedfields:
                filehandle.write('%s\n' % listitem)
        # adding the values in a context variable
        context = {
            'selectedtext': file_name_text,
            'hosp': acc,
            'icu': accdfct,
            'outcome': file_name_model,
            'csvfile': csvfile,
            'pielabelage': pielabelage,
            'piedataage': piedataage,
            'pielabelgen': pielabelgen,
            'piedatagen': piedatagen,
            'pielabelrace': pielabelrace,
            'piedatarace': piedatarace,
            'pielabeleth': pielabeleth,
            'piedataeth': piedataeth,
            'pielabeloutput': pielabeloutput,
            'piedataoutput': piedataoutput,
            'bardatapc' : bardatapc,
            'barlabelpc' : barlabelpc,
        }

        # getting our showdata template
        template = loader.get_template('getdata.html')

        # returing the template
        return HttpResponse(template.render(context, request))
    elif request.POST.get('btnnew') == 'Try out new Model':
        # if post request is not true
        # returing the form template
        cursor = connections['omop'].cursor()
        cursor.execute(
            "SELECT distinct mc.concept_name FROM [UCH_COVID19_LDS].[dbo].[measurement] m "
            "join concept c on c.concept_id=m.value_as_concept_id join concept mc "
            "on mc.concept_id=m.measurement_concept_id where value_as_concept_id ='9191'")
        row = cursor.fetchall()
        cursor.close()
        context = {
            'result': row
        }
        template = loader.get_template('home.html')
        return HttpResponse(template.render(context, request))
    elif (request.POST.get('btnmodel') == 'Predict using model' or request.POST.get(
            'btnmodel') == 'Predict using this model again' or request.POST.get(
        'go') == 'Go'):
        selectedtext = request.POST.get('st')
        modelname = request.POST.get('fn')
        st1 = []
        file_name = os.path.join(os.path.dirname(settings.BASE_DIR), 'omop_ml', selectedtext.lstrip())
        with open(file_name, 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string
                currentPlace = line[:-1]

                # add item to the list
                st1.append(currentPlace)
        # st1 = selectedtext.split(",")
        cohort = st1[0]
        charac1 = st1[1]
        charac2 = st1[2]
        charac3 = st1[3]
        charac4 = st1[4]
        precond1 = st1[5]
        precond2 = st1[6]
        precond3 = st1[7]
        precond4 = st1[8]
        precond5 = st1[9]
        precond6 = st1[10]
        precond7 = st1[11]
        precond8 = st1[12]
        precond9 = st1[13]
        precond10 = st1[14]
        precond11 = st1[15]
        labs1 = st1[16]
        labs2 = st1[17]
        labs3 = st1[18]
        labs4 = st1[19]
        labs5 = st1[20]
        labs6 = st1[21]
        labs7 = st1[22]
        labs8 = st1[23]
        labs9 = st1[24]
        labs10 = st1[25]
        labs11 = st1[26]
        labs12 = st1[27]
        labs13 = st1[28]
        labs14 = st1[29]
        labs15 = st1[30]
        labs16 = st1[31]
        labs17 = st1[32]
        labs18 = st1[33]
        labs19 = st1[34]
        vitals1 = st1[35]
        vitals2 = st1[36]
        vitals3 = st1[37]
        vitals4 = st1[38]
        vitals5 = st1[39]
        vitals6 = st1[40]
        context = {
            'charac1': charac1,
            'modelname': modelname,
            'file_name': file_name,
            'charac2': charac2,
            'charac3': charac3,
            'charac4': charac4,
            'precond1': precond1,
            'precond2': precond2,
            'precond3': precond3,
            'precond4': precond4,
            'precond5': precond5,
            'precond6': precond6,
            'precond7': precond7,
            'precond8': precond8,
            'precond9': precond9,
            'precond10': precond10,
            'precond11': precond11,
            'labs1': labs1,
            'labs2': labs2,
            'labs3': labs3,
            'labs4': labs4,
            'labs5': labs5,
            'labs6': labs6,
            'labs7': labs7,
            'labs8': labs8,
            'labs9': labs9,
            'labs10': labs10,
            'labs11': labs11,
            'labs12': labs12,
            'labs13': labs13,
            'labs14': labs14,
            'labs15': labs15,
            'labs16': labs16,
            'labs17': labs17,
            'labs18': labs18,
            'labs19': labs19,
            'vitals1': vitals1,
            'vitals2': vitals2,
            'vitals3': vitals3,
            'vitals4': vitals4,
            'vitals5': vitals5,
            'vitals6': vitals6,
        }
        template = loader.get_template('modelhome.html')
        return HttpResponse(template.render(context, request))
    elif request.POST.get('btnpredict') == 'Predict':
        file_name = request.POST.get('file_name')
        modelname = request.POST.get('modelname')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        race = request.POST.get('race')
        eth = request.POST.get('eth')
        ht = request.POST.get('ht')
        db = request.POST.get('db')
        kd = request.POST.get('kd')
        ty = request.POST.get('ty')
        ob = request.POST.get('ob')
        ast = request.POST.get('ast')
        lv = request.POST.get('lv')
        lg = request.POST.get('lg')
        hb = request.POST.get('hb')
        hc = request.POST.get('hc')
        hv = request.POST.get('hv')
        wbc = request.POST.get('wbc')
        inr = request.POST.get('inr')
        cal = request.POST.get('cal')
        alb = request.POST.get('alb')
        tp = request.POST.get('tp')
        co = request.POST.get('co')
        cl = request.POST.get('cl')
        cr = request.POST.get('cr')
        alp = request.POST.get('alp')
        alt = request.POST.get('alt')
        astl = request.POST.get('astl')
        bil = request.POST.get('bil')
        hemo = request.POST.get('hemo')
        glu = request.POST.get('glu')
        hema = request.POST.get('hema')
        pla = request.POST.get('pla')
        sod = request.POST.get('sod')
        pot = request.POST.get('pot')
        bun = request.POST.get('bun')
        sbp = request.POST.get('sbp')
        dbp = request.POST.get('dbp')
        hr = request.POST.get('hr')
        rr = request.POST.get('rr')
        temp = request.POST.get('temp')
        o2sat = request.POST.get('o2sat')
        st1 = []
        model_name_full = os.path.join(os.path.dirname(settings.BASE_DIR), 'omop_ml', modelname.lstrip())
        file_name = file_name.lstrip()
        with open(file_name, 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string
                currentPlace = line[:-1]

                # add item to the list
                st1.append(currentPlace)
        # st1 = selectedtext.split(",")
        prlist = []
        prlistname = []
        cohort = st1[0]
        charac1 = st1[1]
        charac2 = st1[2]
        charac3 = st1[3]
        charac4 = st1[4]
        precond1 = st1[5]
        precond2 = st1[6]
        precond3 = st1[7]
        precond4 = st1[8]
        precond5 = st1[9]
        precond6 = st1[10]
        precond7 = st1[11]
        precond8 = st1[12]
        precond9 = st1[13]
        precond10 = st1[14]
        precond11 = st1[15]
        labs1 = st1[16]
        labs2 = st1[17]
        labs3 = st1[18]
        labs4 = st1[19]
        labs5 = st1[20]
        labs6 = st1[21]
        labs7 = st1[22]
        labs8 = st1[23]
        labs9 = st1[24]
        labs10 = st1[25]
        labs11 = st1[26]
        labs12 = st1[27]
        labs13 = st1[28]
        labs14 = st1[29]
        labs15 = st1[30]
        labs16 = st1[31]
        labs17 = st1[32]
        labs18 = st1[33]
        labs19 = st1[34]
        vitals1 = st1[35]
        vitals2 = st1[36]
        vitals3 = st1[37]
        vitals4 = st1[38]
        vitals5 = st1[39]
        vitals6 = st1[40]
        if st1[1] == '1':
            prlist.append(int(age))
            prlistname.append('AGE')
        if st1[2] == '1':
            prlist.append(int(gender))
            prlistname.append('GENDER')
        if st1[3] == '1':
            prlist.append(int(race))
            prlistname.append('RACE')
        if st1[4] == '1':
            prlist.append(int(eth))
            prlistname.append('ETHNICITY')
        if st1[5] == '1':
            prlist.append(int(ht))
            prlistname.append('HYPERTENSION')
        if st1[6] == '1':
            prlist.append(int(db))
            prlistname.append('DIABETES')
        if st1[7] == '1':
            prlist.append(int(kd))
            prlistname.append('KIDNEY')
        if st1[8] == '1':
            prlist.append(int(ty))
            prlistname.append('CANCER')
        if st1[9] == '1':
            prlist.append(int(ob))
            prlistname.append('OBESITY')
        if st1[10] == '1':
            prlist.append(int(ast))
            prlistname.append('ASTHMA')
        if st1[11] == '1':
            prlist.append(int(lv))
            prlistname.append('LIVER')
        if st1[12] == '1':
            prlist.append(int(lg))
            prlistname.append('LUNG')
        if st1[13] == '1':
            prlist.append(int(hb))
            prlistname.append('HEPB')
        if st1[14] == '1':
            prlist.append(int(hc))
            prlistname.append('HEPC')
        if st1[15] == '1':
            prlist.append(int(hv))
            prlistname.append('HIV')
        if st1[16] == '1':
            prlist.append(int(wbc))
            prlistname.append('WBC')
        if st1[17] == '1':
            prlist.append(int(hemo))
            prlistname.append('HEMOGLOBIN')
        if st1[18] == '1':
            prlist.append(int(glu))
            prlistname.append('GLUCOSE')
        if st1[19] == '1':
            prlist.append(int(hema))
            prlistname.append('HEMA')
        if st1[20] == '1':
            prlist.append(int(pla))
            prlistname.append('PLATELET')
        if st1[21] == '1':
            prlist.append(int(sod))
            prlistname.append('SODIUM')
        if st1[22] == '1':
            prlist.append(int(pot))
            prlistname.append('POTASSIUM')
        if st1[23] == '1':
            prlist.append(int(bun))
            prlistname.append('BUN')
        if st1[24] == '1':
            prlist.append(int(inr))
            prlistname.append('PTINR')
        if st1[25] == '1':
            prlist.append(int(cal))
            prlistname.append('CALCIUM')
        if st1[26] == '1':
            prlist.append(int(alb))
            prlistname.append('ALBUMIN')
        if st1[27] == '1':
            prlist.append(int(tp))
            prlistname.append('TOTALPROTEIN')
        if st1[28] == '1':
            prlist.append(int(co))
            prlistname.append('CO2TOTAL')
        if st1[29] == '1':
            prlist.append(int(cl))
            prlistname.append('CHLORIDE')
        if st1[30] == '1':
            prlist.append(int(cr))
            prlistname.append('CREATININE')
        if st1[31] == '1':
            prlist.append(int(alp))
            prlistname.append('ALP')
        if st1[32] == '1':
            prlist.append(int(alt))
            prlistname.append('ALT')
        if st1[33] == '1':
            prlist.append(int(astl))
            prlistname.append('AST')
        if st1[34] == '1':
            prlist.append(int(bil))
            prlistname.append('BILIRUBIN')

        if st1[35] == '1':
            prlist.append(int(sbp))
            prlistname.append('SBP')
        if st1[36] == '1':
            prlist.append(int(dbp))
            prlistname.append('DBP')
        if st1[37] == '1':
            prlist.append(int(hr))
            prlistname.append('HR')
        if st1[38] == '1':
            prlist.append(int(rr))
            prlistname.append('RR')
        if st1[39] == '1':
            prlist.append(int(temp))
            prlistname.append('TEMP')
        if st1[40] == '1':
            prlist.append(int(o2sat))
            prlistname.append('O2SAT')
        trained_model = load_ml_model(model_name_full)
        prlist = [prlist, prlist]
        prlistdf = DataFrame(prlist, columns=prlistname)

        # .predict and .predict_proba take in either:
        # A pandas DataFrame
        # A list of dictionaries
        # A single dictionary (optimized for speed in production evironments)
        predictions = trained_model.predict(prlistdf)

        output = round(predictions[0])
        if output == 0:
            output_text = 'Low'
        else:
            output_text = 'High'

        context = {
            'modelname': modelname,
            'file_name': file_name,
            'hosp': output_text,
            'icu': 'low',
            'outcome': 'low'

        }
        template = loader.get_template('modelprediction.html')
        return HttpResponse(template.render(context, request))

    else:
        # if post request is not true
        # returing the form template
        template = loader.get_template('home.html')
        return HttpResponse(template.render())


@csrf_exempt
def apphome(request):
    from os import listdir
    from os.path import isfile, join
    mypath = r'c:\users\aalurwar\PycharmProjects\omop_ml\models'
    # onlyfiles = [f for f in listdir(mypath) if isfile if f.endswith(".txt") == True (join(mypath, f))]
    onlyfiles = []
    for file in os.listdir(mypath):
        if file.endswith(".txt"):
            onlyfiles.append(file)
    labels = []
    data = []
    labels.append('Aniket')
    labels.append('Mary')
    data.append(85)
    data.append(95)
    context = {
        'pathfile': onlyfiles,
        'labels': labels,
        'data': data,
    }
    template = loader.get_template('apphome.html')
    return HttpResponse(template.render(context, request))
