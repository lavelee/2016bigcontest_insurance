-- CLAIM
CREATE TABLE `insurance`.`CLAIM` (
	`CUST_ID`         MEDIUMINT  NULL     COMMENT '고객을 구분하는 고유번호', -- 고객번호
	`POLY_NO`         MEDIUMINT  NULL     COMMENT '청약서번호이면서 동시에 계약성립후에는 증권번호로 사용
	', -- 보험계약번호
	`ACCI_OCCP_GRP1`  TINYINT    NULL     COMMENT '총 8개직업군으로 분류한 코드(사고 당시)
	', -- 사고시직업_대분류
	`ACCI_OCCP_GRP2`  TINYINT    NULL     COMMENT '총 25개직업군으로 분류한 코드(사고 당시)
	', -- 사고시직업_소분류
	`CHANG_FP_YN`     TINYINT    NULL     COMMENT '가입한 Fp와 보험금 청구시 FP 가 다른가?', -- 모집FP=청구FP?
	`CNTT_RECP_SQNO`  BIGINT     NOT NULL COMMENT '사고접수에 대해 해당 계약건별로 부여하는 번호
	', -- 사고접수번호
	`RECP_DATE`       DATE       NULL     COMMENT '사고가 접수된 일자
	', -- 사고접수일자
	`ORIG_RESN_DATE`  DATE       NULL     COMMENT '사고접수시 해당 사고의 최초 사유발생일자 
	', -- 근본원인발생일자
	`RESN_DATE`       DATE       NULL     COMMENT '보험금 지급사유 발생일자
	', -- 지급사유충족일자
	`CRNT_PROG_DVSN`  TINYINT    NULL     COMMENT '현재진행구분 상태 구분 
	 - 접수(11), 심사배정(21), 심사(22), 심사결재(23), 조사(32), 조사결재(33)', -- 청구진행상태
	`ACCI_DVSN`       TINYINT    NULL     COMMENT '"사고원인을 구분함
	 - 재해(1), 교통재해(2), 질병(3)"
	', -- 사고종류
	`CAUS_CODE`       MEDIUMINT  NULL     COMMENT '사고의 원인에 해당하는 사인코드 
	', -- 사고원인코드
	`CAUS_CODE_DTAL`  TINYINT    NULL     COMMENT '사고의 원인에 해당하는 사인코드_상세정보
	''#'' 값은 대부분 병원 진단서 등에서 해당 내용의 기재가 누락된 경우에 해당하며, 담당자의 기재 오류 또는 실제 상세원인이 불분명할 경우까지 모두 포함합니다. ', -- 사고원인세부
	`DSAS_NAME`       MEDIUMTEXT NULL     COMMENT '병명
	', -- 병명
	`DMND_RESN_CODE`  TINYINT    NULL     COMMENT '"지급청구의 원인이 되는 사유코드  
	 - 사망(01), 입원(02), 통원(03), 장해(04), 수술(05), 진단(06), 치료(07), 해지/무효(09)"', -- 청구사유코드
	`DMND_RSCD_SQNO`  TINYINT    NOT NULL COMMENT '동일 증번, 동일한 청구사유이지만 사유일자가 다른 경우 일련번호를 1씩 증가시킴. 
	', -- 보험청구번호
	`HOSP_OTPA_STDT`  DATE       NULL     COMMENT '입원시작일, 통원은 통원시작일 (입원은 무조건 연속된일자만 관리됨)
	', -- 입원통원시작일
	`HOSP_OTPA_ENDT`  DATE       NULL     COMMENT '입원종료일, 통원은 통원종료일  
	', -- 입원통원종료일
	`RESL_CD1`        MEDIUMINT  NULL     COMMENT '최종원인코드', -- 최종원인코드
	`RESL_NM1`        MEDIUMTEXT NULL     COMMENT '결과내용
	', -- 확정원인내용
	`VLID_HOSP_OTDA`  MEDIUMINT  NULL     COMMENT '보험금지급대상인 입원일수 또는 통원일수  
	', -- 지급대상입/통원일수
	`HOUSE_HOSP_DIST` FLOAT      NULL     COMMENT '고객 거주지와 병원까지의 거리(km)
	', -- 거주지-병원km
	`HOSP_CODE`       INT        NULL     COMMENT '병원코드
	', -- 병원코드
	`ACCI_HOSP_ADDR`  TINYINT    NULL     COMMENT '병원주소', -- 병원지역
	`HOSP_SPEC_DVSN`  TINYINT    NULL     COMMENT '"병원종별구분
	 - 종합병원(10), 병원(20), 요양병원(25), 의원(30), 치과병원(40), 치과의원(45), 보건의료원(60), ', -- 병원종별구분
	`CHME_LICE_NO`    INT        NULL     COMMENT '의사면허번호
	', -- 담당의사번호
	`PAYM_DATE`       DATE       NULL     COMMENT '보험금 지급일자
	', -- 보험금지급일자
	`DMND_AMT`        INT        NULL     COMMENT '사고보험금청구금액  
	', -- 보험금청구액수
	`PAYM_AMT`        INT        NULL     COMMENT '실지급금액  
	', -- 실제지급금액
	`PMMI_DLNG_YN`    TINYINT    NULL     COMMENT '실손처리여부', -- 실손처리?
	`SELF_CHAM`       INT        NULL     COMMENT '국민건강보험 적용 금액 중 환자 부담 금액
	', -- 본인부담금
	`NON_PAY`         INT        NULL     COMMENT '국민건강보험 미적용 금액
	', -- 비급여액
	`TAMT_SFCA`       INT        NULL     COMMENT '국민건강보험 미적용 금액
	', -- 전액본인부담금
	`PATT_CHRG_TOTA`  INT        NULL     COMMENT '본인부담금 + 비급여 + 전액본인부담금 
	', -- 환자부담총액
	`DSCT_AMT`        INT        NULL     COMMENT '병원에서 할인해주는 비용
	', -- 병원할인액
	`COUNT_TRMT_ITEM` TINYINT    NULL     COMMENT '실손영수증 내 진료과목의 개수
	', -- 청구시 진료과목수
	`DCAF_CMPS_XCPA`  INT        NULL     COMMENT '실손 상품의 경우 상품의 특성상 약관상으로 일정한 보상제외 항목을 포함하고 있는데요. 이러한 보상제외 항목에 해당하는 금액을 의미합니다.
	그리하여 실제 보험사는 피보험자에게 발생한 총 비용에서 보상제외 항목에 해당하는 금액을 제외한 금액만을 보상하게 됩니다', --  실손상품에서 보상제외금액
	`NON_PAY_RATIO`   FLOAT      NULL     COMMENT '(비급여 + 전액본인부담금) / (환자부담총액) = (비급여 + 전액본인부담금) / (본인부담금 + 비급여 + 전액본인부담금)
	', -- 실손비급여비율
	`HEED_HOSP_YN`    TINYINT    NULL     COMMENT '금감원 유의 병원 대상 여부 
	' -- 금감원 유의병원?
)
COMMENT 'CLAIM';

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `PK_CLAIM` -- CLAIM 기본키
		PRIMARY KEY (
			`CNTT_RECP_SQNO` -- 사고접수번호
		);

-- CNTT
CREATE TABLE `insurance`.`CNTT` (
	`POLY_NO`        MEDIUMINT NULL COMMENT '청약서번호이면서 동시에 계약성립후에는 증권번호로 사용
	', -- 보험계약번호
	`CUST_ID`        MEDIUMINT NULL COMMENT '고객을 구분하는 고유번호
	', -- 고객번호
	`CUST_ROLE`      TINYINT   NULL COMMENT '"계약에 있어 고객의 역할을 구분한 코드
	계약자이나 주피보험자는 아님(0) // 계약자이며 주피보험자임(1) 
	// 계약자는 아', -- 고객역할코드
	`IRKD_CODE_DTAL` MEDIUMINT NULL COMMENT '상품에 부여된 번호
	', -- 고유상품번호
	`IRKD_CODE_ITEM` MEDIUMINT NULL COMMENT '상품에 부여된 번호이며 보험료등이 변경되거나 상품이 개정되는 경우 변경됨
	', -- 상품버전
	`GOOD_CLSF_CDNM` TINYINT   NULL COMMENT '해당 상품이 어떠한 분류에 해당하는지를 설명 (총 18가지이며 중복없음)
	', -- 상품분류18종
	`CNTT_YM`        DATE      NULL COMMENT '보험계약이 체결된 연월을 6자리로 표기함
	', -- 계약년월
	`CLLT_FP_PRNO`   INT       NULL COMMENT '보험설계사(FP) 또는 내근직원에게 부여되는 고유번호 
	', -- FP사번
	`REAL_PAYM_TERM` MEDIUMINT NULL COMMENT '보험료를 납입하기로 한 기간(년) (0의 경우 일시납//999의 경우 종신납)
	', -- 보험료납입계약기간
	`SALE_CHNL_CODE` TINYINT   NULL COMMENT '"고객이 보험상품을 구매한 채널에 대한 코드
	설계사(1),법인(2),홈페이지(3),전화영업(4),방카슈랑스(5),남성전문조직(6),보험대리점(7)"
	
	', -- 판매채널코드
	`CNTT_STAT_CODE` TINYINT   NULL COMMENT '"계약의 현재상태를 나타내는 코드
	유지(1),완납(2),납입면제(3),효력상실(4),만기경과(9)
	만기지급(A),해약(B),사망감소( C ),장해감소(D),해지 (E )
	무효(G),정산(H),청약철회(I),반송(J),부활취소(L)"', -- 계약상태코드
	`EXPR_YM`        DATE      NULL COMMENT '보험기간이 끝나는 연월(종신보험의 경우 999912)
	', -- 만기년월
	`EXTN_YM`        DATE      NULL COMMENT '보험이 소멸한 연월(소멸한 적이 없으면 NULL)
	', -- 소멸했다면연월
	`LAPS_YM`        DATE      NULL COMMENT '보험이 실효된 연월(실효된 적이 없으면 NULL)
	', -- 실효했다면연월
	`PAYM_CYCL_CODE` TINYINT   NULL COMMENT '"보험료의 납입주기 코드
	(0: 일시납, 1:월납,3:3개월에 한번씩 납입,6:6개월에 한번씩 보험료 납입,12:1년에 한번씩 보험료 납입)"
	
	', -- 납입주기코드
	`MAIN_INSR_AMT`  INT       NULL COMMENT '주계약의 보험금액(단위:원)
	', -- 주계약보장액
	`SUM_ORIG_PREM`  INT       NULL COMMENT '계약(주계약 + 특약)의 단위납입 보험료
	', -- 회당보험료납입액
	`RECP_PUBL`      MEDIUMINT NULL COMMENT '보험을 가입하기 위한 청약서를 발행하고 접수하기까지 소요된 기간 (일)
	', -- 신청-청약 소요시간
	`CNTT_RECP`      MEDIUMINT NULL COMMENT '청약서를 접수하고 난 이후 실제 계약기간 까지의 소요된 기간 (일)
	', -- 청약-계약 소요시간
	`MNTH_INCM_AMT`  INT       NULL COMMENT '청약서에 기재한 월소득금액 (원)
	', -- 청약서 기재소득
	`DISTANCE`       MEDIUMINT NULL COMMENT 'FP와 고객간 거주지의 거리(단위 : KM)
	' -- FP와 고객 거주지거리
)
COMMENT 'CNTT';

-- FMLY
CREATE TABLE `insurance`.`FMLY` (
	`CUST_ID`        MEDIUMINT NULL COMMENT '고객번호', -- 고객번호
	`ACCI_OCCP_GRP2` MEDIUMINT NULL COMMENT '가족고객번호', -- 가족고객번호
	`FMLY_RELN_CODE` TINYINT   NULL COMMENT '가족관계코드' -- 가족관계코드
)
COMMENT 'FMLY';

-- CUST
CREATE TABLE `insurance`.`CUST` (
	`CUST_ID`          MEDIUMINT NOT NULL COMMENT '고객을 구분하는 고유번호
	', -- 고객번호
	`DIVIDED_SET`      TINYINT   NULL     COMMENT '학습용 Set의 경우 1번 // 평가용 Set의 경우 2번을 부여
	', -- 학습데이터?
	`SIU_CUST_YN`      TINYINT   NULL     COMMENT '보험사기자?', -- 보험사기자?
	`SEX`              TINYINT   NULL     COMMENT '성별 1은 ''남성'' 2는 ''여성''
	', -- 성별
	`AGE`              TINYINT   NULL     COMMENT '고객연령
	', -- 나이
	`RESI_COST`        BIGINT    NULL     COMMENT '고객의 거주지 주택가격 추정값 (단위 : 만원) (0 : 추정불가)
	', -- 주택가격(만원)
	`RESI_TYPE_CODE`   TINYINT   NULL     COMMENT '"고객의 거주지 형태
	 - 일반단독주택(11), 다가구단독주택(12), 영업겸용단독주택(13), 아파트(20),연립_다가구주택(30)
	   상가등 비거주용건물(40),오피스텔(50),숙박업소의 객실 또는 판자집 등(60),기숙사(70),그외(99)"
	
	', -- 거주형태
	`FP_CAREER`        TINYINT   NULL     COMMENT 'FP경력자?', -- FP경력자?
	`CUST_RGST`        DATE      NULL     COMMENT '최초 당사의 고객으로써의 등록연월
	', -- 등록연월
	`CTPR`             TINYINT   NULL     COMMENT '거주시도', -- 거주시도
	`OCCP_GRP1`        TINYINT   NULL     COMMENT '1	1.주부	
	2	2.자영업	
	3	3.사무직	
	4	4.전문직	
	5	5.서비스	
	6	6.제조업	
	7	7.1차산업	
	8	8.기타	
	', -- 직업대분류8
	`OCCP_GRP2`        TINYINT   NULL     COMMENT '1	1차산업 종사자
	2	2차산업 종사자
	3	3차산업 종사자
	4	고소득 전문직
	5	고소득의료직
	6	고위 공무원
	7	공무원
	8	교사
	9	교육관련직
	10	기업/단체 임원
	11	기타
	12	단순 노무직
	13	단순 사무직
	14	대학교수/강사
	15	법무직 종사자
	16	사무직
	17	예체능계 종사자
	18	운전직
	19	의료직 종사자
	20	자영업
	21	전문직
	22	종교인/역술인
	23	주부
	24	학생
	25	학자/연구직', -- 직업소분류25
	`TOTALPREM`        INT       NULL     COMMENT '고객이 지금까지 당사에 실제 납입한 총 보험료의 합계
	', -- 납입총보험료
	`MINCRDT`          TINYINT   NULL     COMMENT '신용등급 확인 중 최소값 (미확인의 경우 6등급에 포함)
	', -- 최저신용등급
	`MAXCRDT`          TINYINT   NULL     COMMENT '신용등급 확인 중 최대값 (미확인의 경우 6등급에 포함)
	', -- 최대신용등급
	`WEDD_YN`          TINYINT   NULL     COMMENT '결혼?', -- 결혼?
	`MATE_OCCP_GRP2`   TINYINT   NULL     COMMENT '배우자직업8', -- 배우자직업8
	`MATE_OCCP_GRP1`   TINYINT   NULL     COMMENT '배우자직업25', -- 배우자직업25
	`CHLD_CNT`         TINYINT   NULL     COMMENT '고객의 자녀 수
	', -- 자녀수
	`LTBN_CHLD_AGE`    TINYINT   NULL     COMMENT '고객의 막내자녀 연령
	', -- 막내나이
	`MAX_PAYM_YM`      DATE      NULL     COMMENT '당사에 최대규모의 보험료를 납입했던 연월
	', -- 최대보험료낸연월
	`MAX_PRM`          INT       NULL     COMMENT '당사에 최대규모의 보험료를 납입했던 월보험료 수준
	', -- 최대보험료얼마
	`CUST_INCM`        INT       NULL     COMMENT '고객의 연령/직업/보험료 수준등을 통한 고객의 개인 연소득 추정금액(원본은 단위 만원인데 원으로 변경함)', -- 개인소득추정
	`RCBASE_HSHD_INCM` INT       NULL     COMMENT '고객의 주택가격을 우선하여 정한 가구소득 추정금액 (원본단위 만원에서 원으로 변경함)
	', -- 가계소득추정(BY주택)
	`JPBASE_HSHD_INCM` INT       NULL     COMMENT '고객의 직업 및 납입보험료 수준을 우선하여 정한 가구소득 추정금액(원본단위 만원에서 원으로 변경함)
	' -- 가계소득추정(BY직업+보험료)
)
COMMENT 'CUST';

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `PK_CUST` -- CUST 기본키
		PRIMARY KEY (
			`CUST_ID` -- 고객번호
		);

-- FPINFO
CREATE TABLE `insurance`.`FPINFO` (
	`CLLT_FP_PRNO` INT     NOT NULL COMMENT '보험설계사(FP) 또는 내근직원에게 부여되는 고유번호
	', -- FP사번
	`INCB_DVSN`    TINYINT NULL     COMMENT '직원이 현재 재직중인지 해촉인지 확인 코드(''R''=해촉, ''P''=재적 ''D''=내근직원, ''C''=위촉취소, ''#''=기타)
	', -- FP고용형태
	`ETRS_YM`      DATE    NULL     COMMENT '보험설계사(FP)의 입사 년월
	', -- FP입사년월
	`FIRE_YM`      DATE    NULL     COMMENT '보험설계사(FP)의 퇴직 년월
	', -- FP퇴직년월
	`BEFO_JOB`     TINYINT NULL     COMMENT '보험설계사(FP)가 입사하여 보험설계사 일을 하기 전 직업
	', -- FP이전직업
	`EDGB`         TINYINT NULL     COMMENT '보험설계사(FP)의 최종학력
	', -- FP최종학력
	`BRCH_CODE`    INT     NULL     COMMENT '보험설계사(FP)가 근무하는 소속 지점 기관코드
	' -- 소속지점코드
)
COMMENT 'FPINFO';

-- FPINFO
ALTER TABLE `insurance`.`FPINFO`
	ADD CONSTRAINT `PK_FPINFO` -- FPINFO 기본키
		PRIMARY KEY (
			`CLLT_FP_PRNO` -- FP사번
		);

-- 직업대분류(8종)
CREATE TABLE `insurance`.`JOB8` (
	`ACCI_OCCP_GRP1` TINYINT  NOT NULL COMMENT '1	1.주부
	2	2.자영업
	3	3.사무직
	4	4.전문직
	5	5.서비스
	6	6.제조업
	7	7.1차산업
	8	8.기타', -- 직업대분류8
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '직업대분류(8종)';

-- 직업대분류(8종)
ALTER TABLE `insurance`.`JOB8`
	ADD CONSTRAINT `PK_JOB8` -- 직업대분류(8종) 기본키
		PRIMARY KEY (
			`ACCI_OCCP_GRP1` -- 직업대분류8
		);

-- 직업소분류(25종)
CREATE TABLE `insurance`.`JOB25` (
	`ACCI_OCCP_GRP2` TINYINT  NOT NULL COMMENT 'NO	ACCI_OCCP_GRP2
	1	1차산업 종사자
	2	2차산업 종사자
	3	3차산업 종사자
	4	고소득 전문직
	5	고소득의료직
	6	고위 공무원
	7	공무원
	8	교사
	9	교육관련직
	10	기업/단체 임원
	11	기타
	12	단순 노무직
	13	단순 사무직
	14	대학교수/강사
	15	법무직 종사자
	16	사무직
	17	예체능계 종사자
	18	운전직
	19	의료직 종사자
	20	자영업
	21	전문직
	22	종교인/역술인
	23	주부
	24	학생
	25	학자/연구직
	26	 (빈칸)', -- 직업소분류25
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '직업소분류(25종)';

-- 직업소분류(25종)
ALTER TABLE `insurance`.`JOB25`
	ADD CONSTRAINT `PK_JOB25` -- 직업소분류(25종) 기본키
		PRIMARY KEY (
			`ACCI_OCCP_GRP2` -- 직업소분류25
		);

-- YN
CREATE TABLE `insurance`.`YN` (
	`YN`      TINYINT  NOT NULL COMMENT 'Y:1 N:0', -- YN
	`CONTEXT` TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT 'YN';

-- YN
ALTER TABLE `insurance`.`YN`
	ADD CONSTRAINT `PK_YN` -- YN 기본키
		PRIMARY KEY (
			`YN` -- YN
		);

-- 청구진행상태
CREATE TABLE `insurance`.`CRNT_PROG_DVSN` (
	`CRNT_PROG_DVSN` TINYINT  NOT NULL COMMENT '현재진행구분 상태 구분 
	 - 접수(11), 심사배정(21), 심사(22), 심사결재(23), 조사(32), 조사결재(33)', -- 청구진행상태
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '청구진행상태';

-- 청구진행상태
ALTER TABLE `insurance`.`CRNT_PROG_DVSN`
	ADD CONSTRAINT `PK_CRNT_PROG_DVSN` -- 청구진행상태 기본키
		PRIMARY KEY (
			`CRNT_PROG_DVSN` -- 청구진행상태
		);

-- 사고원인대분류
CREATE TABLE `insurance`.`CAUS_1` (
	`ACCI_DVSN` TINYINT  NOT NULL COMMENT '"사고원인을 구분함
	 - 재해(1), 교통재해(2), 질병(3)"
	
	', -- 사고원인대분류
	`CONTEXT`   TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '사고원인대분류';

-- 사고원인대분류
ALTER TABLE `insurance`.`CAUS_1`
	ADD CONSTRAINT `PK_CAUS_1` -- 사고원인대분류 기본키
		PRIMARY KEY (
			`ACCI_DVSN` -- 사고원인대분류
		);

-- 사고원인소분류
CREATE TABLE `insurance`.`CAUS_2` (
	`CAUS_CODE` MEDIUMINT NOT NULL COMMENT '사고의 원인에 해당하는 사인코드 
	', -- 사고원인코드
	`CONTEXT`   TINYTEXT  NULL     COMMENT '내용' -- 내용
)
COMMENT '사고원인소분류';

-- 사고원인소분류
ALTER TABLE `insurance`.`CAUS_2`
	ADD CONSTRAINT `PK_CAUS_2` -- 사고원인소분류 기본키
		PRIMARY KEY (
			`CAUS_CODE` -- 사고원인코드
		);

-- 사고원인세부특징
CREATE TABLE `insurance`.`CAUS_3` (
	`CAUS_CODE_DTAL` TINYINT  NOT NULL COMMENT '사고의 원인에 해당하는 사인코드_상세정보
	', -- 사고원인세부
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '사고원인세부특징';

-- 사고원인세부특징
ALTER TABLE `insurance`.`CAUS_3`
	ADD CONSTRAINT `PK_CAUS_3` -- 사고원인세부특징 기본키
		PRIMARY KEY (
			`CAUS_CODE_DTAL` -- 사고원인세부
		);

-- 청구사유
CREATE TABLE `insurance`.`DMND_RESN_CODE` (
	`DMND_RESN_CODE` TINYINT  NOT NULL COMMENT '"지급청구의 원인이 되는 사유코드  
	 - 사망(01), 입원(02), 통원(03), 장해(04), 수술(05), 진단(06), 치료(07), 해지/무효(09)"
	
	', -- 청구사유코드
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '청구사유';

-- 청구사유
ALTER TABLE `insurance`.`DMND_RESN_CODE`
	ADD CONSTRAINT `PK_DMND_RESN_CODE` -- 청구사유 기본키
		PRIMARY KEY (
			`DMND_RESN_CODE` -- 청구사유코드
		);

-- 지역
CREATE TABLE `insurance`.`LOCALE` (
	`ACCI_HOSP_DIST` TINYINT  NOT NULL COMMENT '병원지역
	1	
	2	강원
	3	경기
	4	경남
	5	경북
	6	광주
	7	대구
	8	대전
	9	부산
	10	서울
	11	세종
	12	울산
	13	인천
	14	전남
	15	전북
	16	제주
	17	충남
	18	충북
	', -- 지역코드
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '지역';

-- 지역
ALTER TABLE `insurance`.`LOCALE`
	ADD CONSTRAINT `PK_LOCALE` -- 지역 기본키
		PRIMARY KEY (
			`ACCI_HOSP_DIST` -- 지역코드
		);

-- 병원종별구분
CREATE TABLE `insurance`.`HOSP_SPEC_DVSN` (
	`HOSP_SPEC_DVSN` TINYINT  NOT NULL COMMENT '"병원종별구분
	 - 종합병원(10), 병원(20), 요양병원(25), 의원(30), 치과병원(40), 치과의원(45), 보건의료원(60), 
	   약국(70), 한방병원(80), 한의원(85), 해외(90), 의료기관이외(95)"
	
	', -- 병원종별구분
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '병원종별구분';

-- 병원종별구분
ALTER TABLE `insurance`.`HOSP_SPEC_DVSN`
	ADD CONSTRAINT `PK_HOSP_SPEC_DVSN` -- 병원종별구분 기본키
		PRIMARY KEY (
			`HOSP_SPEC_DVSN` -- 병원종별구분
		);

-- 가족관계
CREATE TABLE `insurance`.`FMLY_RELN_CODE` (
	`FMLY_RELN_CODE` TINYINT  NOT NULL COMMENT '"가족관계코드
	 - 본인(11), 배우자(12), 부모(13), 자녀(14), 조부모(15), 손자(녀)(16), 형제자매(17), 배우자부모(18), 
	   외조부모(19), 외손자(녀)(20), 기타(99)"
	
	', -- 가족관계코드
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '가족관계';

-- 가족관계
ALTER TABLE `insurance`.`FMLY_RELN_CODE`
	ADD CONSTRAINT `PK_FMLY_RELN_CODE` -- 가족관계 기본키
		PRIMARY KEY (
			`FMLY_RELN_CODE` -- 가족관계코드
		);

-- FP고용형태
CREATE TABLE `insurance`.`INCB_DVSN` (
	`INCB_DVSN`     TINYINT  NOT NULL COMMENT '직원이 현재 재직중인지 해촉인지 확인 코드(''R''=해촉, ''P''=재적 ''D''=내근직원, ''C''=위촉취소, ''#''=기타)
	', -- FP고용형태
	`ORIGINAL_CODE` TINYTEXT NULL     COMMENT '원본코드', -- 원본코드
	`CONTEXT`       TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT 'FP고용형태';

-- FP고용형태
ALTER TABLE `insurance`.`INCB_DVSN`
	ADD CONSTRAINT `PK_INCB_DVSN` -- FP고용형태 기본키
		PRIMARY KEY (
			`INCB_DVSN` -- FP고용형태
		);

-- FP이전직업
CREATE TABLE `insurance`.`BEFO_JOB` (
	`BEFO_JOB` TINYINT  NOT NULL COMMENT '보험설계사(FP)가 입사하여 보험설계사 일을 하기 전 직업
	', -- FP이전직업
	`CONTEXT`  TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT 'FP이전직업';

-- FP이전직업
ALTER TABLE `insurance`.`BEFO_JOB`
	ADD CONSTRAINT `PK_BEFO_JOB` -- FP이전직업 기본키
		PRIMARY KEY (
			`BEFO_JOB` -- FP이전직업
		);

-- FP최종학력
CREATE TABLE `insurance`.`EDGB` (
	`EDGB`    TINYINT  NOT NULL COMMENT '보험설계사(FP)의 최종학력
	', -- FP최종학력
	`CONTEXT` TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT 'FP최종학력';

-- FP최종학력
ALTER TABLE `insurance`.`EDGB`
	ADD CONSTRAINT `PK_EDGB` -- FP최종학력 기본키
		PRIMARY KEY (
			`EDGB` -- FP최종학력
		);

-- 고객역할코드
CREATE TABLE `insurance`.`CUST_ROLE` (
	`CUST_ROLE` TINYINT  NOT NULL COMMENT '"계약에 있어 고객의 역할을 구분한 코드
	계약자이나 주피보험자는 아님(0) // 계약자이며 주피보험자임(1) 
	// 계약자는 아니지만 주피보험자임(2) //주피보험자는 아니지만 피보험자임(21)
	// 피보험자는 아니지만 생존수익자(3)// 피보험자 및 생존수익자는 아니지만 입원장해수익자(4)
	// 피보험자는 생존급부의 수익자는 아니지만 사망수익자(5)"
	
	', -- 고객역할코드
	`CONTEXT`   TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '고객역할코드';

-- 고객역할코드
ALTER TABLE `insurance`.`CUST_ROLE`
	ADD CONSTRAINT `PK_CUST_ROLE` -- 고객역할코드 기본키
		PRIMARY KEY (
			`CUST_ROLE` -- 고객역할코드
		);

-- 상품분류18종
CREATE TABLE `insurance`.`GOOD_CLSF_CDNM` (
	`GOOD_CLSF_CDNM` TINYINT  NOT NULL COMMENT '해당 상품이 어떠한 분류에 해당하는지를 설명 (총 18가지이며 중복없음)
	', -- 상품분류18종
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '상품분류18종';

-- 상품분류18종
ALTER TABLE `insurance`.`GOOD_CLSF_CDNM`
	ADD CONSTRAINT `PK_GOOD_CLSF_CDNM` -- 상품분류18종 기본키
		PRIMARY KEY (
			`GOOD_CLSF_CDNM` -- 상품분류18종
		);

-- 판매채널코드
CREATE TABLE `insurance`.`SALE_CHNL_CODE` (
	`SALE_CHNL_CODE` TINYINT  NOT NULL COMMENT '"고객이 보험상품을 구매한 채널에 대한 코드
	설계사(1),법인(2),홈페이지(3),전화영업(4),방카슈랑스(5),남성전문조직(6),보험대리점(7)"
	', -- 판매채널코드
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '판매채널코드';

-- 판매채널코드
ALTER TABLE `insurance`.`SALE_CHNL_CODE`
	ADD CONSTRAINT `PK_SALE_CHNL_CODE` -- 판매채널코드 기본키
		PRIMARY KEY (
			`SALE_CHNL_CODE` -- 판매채널코드
		);

-- 계약상태
CREATE TABLE `insurance`.`CNTT_STAT_CODE` (
	`CNTT_STAT_CODE` TINYINT  NOT NULL COMMENT '"계약의 현재상태를 나타내는 코드
	유지(1),완납(2),납입면제(3),효력상실(4),만기경과(9)
	만기지급(A),해약(B),사망감소( C ),장해감소(D),해지 (E )
	무효(G),정산(H),청약철회(I),반송(J),부활취소(L)"
	
	', -- 계약상태코드
	`ORIGINAL_CODE`  TINYTEXT NULL     COMMENT '원본코드', -- 원본코드
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '계약상태';

-- 계약상태
ALTER TABLE `insurance`.`CNTT_STAT_CODE`
	ADD CONSTRAINT `PK_CNTT_STAT_CODE` -- 계약상태 기본키
		PRIMARY KEY (
			`CNTT_STAT_CODE` -- 계약상태코드
		);

-- 납입주기
CREATE TABLE `insurance`.`PAYM_CYCL_CODE` (
	`PAYM_CYCL_CODE` TINYINT  NOT NULL COMMENT '"보험료의 납입주기 코드
	(0: 일시납, 1:월납,3:3개월에 한번씩 납입,6:6개월에 한번씩 보험료 납입,12:1년에 한번씩 보험료 납입)"
	
	', -- 납입주기코드
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '납입주기';

-- 납입주기
ALTER TABLE `insurance`.`PAYM_CYCL_CODE`
	ADD CONSTRAINT `PK_PAYM_CYCL_CODE` -- 납입주기 기본키
		PRIMARY KEY (
			`PAYM_CYCL_CODE` -- 납입주기코드
		);

-- 데이터구분
CREATE TABLE `insurance`.`DIVIDED_SET` (
	`DIVIDED_SET` TINYINT  NOT NULL COMMENT '학습용 Set의 경우 1번 // 평가용 Set의 경우 2번을 부여
	', -- 학습데이터?
	`CONTEXT`     TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '데이터구분';

-- 데이터구분
ALTER TABLE `insurance`.`DIVIDED_SET`
	ADD CONSTRAINT `PK_DIVIDED_SET` -- 데이터구분 기본키
		PRIMARY KEY (
			`DIVIDED_SET` -- 학습데이터?
		);

-- 임시 테이블2
CREATE TABLE `insurance`.`SIU_CUST_YN` (
	`SIU_CUST_YN` TINYINT  NOT NULL COMMENT 'Y의 경우 ''보험사기자'' / N의 경우 ''일반고객'' /평가용 Set에는 미부여
	', -- 보험사기자?
	`CONTEXT`     TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '임시 테이블2';

-- 임시 테이블2
ALTER TABLE `insurance`.`SIU_CUST_YN`
	ADD CONSTRAINT `PK_SIU_CUST_YN` -- 임시 테이블2 기본키
		PRIMARY KEY (
			`SIU_CUST_YN` -- 보험사기자?
		);

-- 남/여?
CREATE TABLE `insurance`.`SEX` (
	`SEX`     TINYINT  NOT NULL COMMENT '성별 1은 ''남성'' 2는 ''여성''
	', -- 성별
	`CONTEXT` TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '남/여?';

-- 남/여?
ALTER TABLE `insurance`.`SEX`
	ADD CONSTRAINT `PK_SEX` -- 남/여? 기본키
		PRIMARY KEY (
			`SEX` -- 성별
		);

-- 거주형태
CREATE TABLE `insurance`.`RESI_TYPE_CODE` (
	`RESI_TYPE_CODE` TINYINT  NOT NULL COMMENT '"고객의 거주지 형태
	 - 일반단독주택(11), 다가구단독주택(12), 영업겸용단독주택(13), 아파트(20),연립_다가구주택(30)
	   상가등 비거주용건물(40),오피스텔(50),숙박업소의 객실 또는 판자집 등(60),기숙사(70),그외(99)"
	
	', -- 거주형태
	`CONTEXT`        TINYTEXT NULL     COMMENT '내용' -- 내용
)
COMMENT '거주형태';

-- 거주형태
ALTER TABLE `insurance`.`RESI_TYPE_CODE`
	ADD CONSTRAINT `PK_RESI_TYPE_CODE` -- 거주형태 기본키
		PRIMARY KEY (
			`RESI_TYPE_CODE` -- 거주형태
		);

-- 임시 테이블
CREATE TABLE `insurance`.`POLY_NO` (
	`POLY_NO` MEDIUMINT NOT NULL COMMENT '청약서번호이면서 동시에 계약성립후에는 증권번호로 사용
	' -- 보험계약번호
)
COMMENT '임시 테이블';

-- 임시 테이블
ALTER TABLE `insurance`.`POLY_NO`
	ADD CONSTRAINT `PK_POLY_NO` -- 임시 테이블 기본키
		PRIMARY KEY (
			`POLY_NO` -- 보험계약번호
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_JOB8_TO_CLAIM` -- 직업대분류(8종) -> CLAIM
		FOREIGN KEY (
			`ACCI_OCCP_GRP1` -- 사고시직업_대분류
		)
		REFERENCES `insurance`.`JOB8` ( -- 직업대분류(8종)
			`ACCI_OCCP_GRP1` -- 직업대분류8
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_CUST_TO_CLAIM` -- CUST -> CLAIM
		FOREIGN KEY (
			`CUST_ID` -- 고객번호
		)
		REFERENCES `insurance`.`CUST` ( -- CUST
			`CUST_ID` -- 고객번호
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_JOB25_TO_CLAIM` -- 직업소분류(25종) -> CLAIM
		FOREIGN KEY (
			`ACCI_OCCP_GRP2` -- 사고시직업_소분류
		)
		REFERENCES `insurance`.`JOB25` ( -- 직업소분류(25종)
			`ACCI_OCCP_GRP2` -- 직업소분류25
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_YN_TO_CLAIM` -- YN -> CLAIM
		FOREIGN KEY (
			`CHANG_FP_YN` -- 모집FP=청구FP?
		)
		REFERENCES `insurance`.`YN` ( -- YN
			`YN` -- YN
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_CRNT_PROG_DVSN_TO_CLAIM` -- 청구진행상태 -> CLAIM
		FOREIGN KEY (
			`CRNT_PROG_DVSN` -- 청구진행상태
		)
		REFERENCES `insurance`.`CRNT_PROG_DVSN` ( -- 청구진행상태
			`CRNT_PROG_DVSN` -- 청구진행상태
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_CAUS_1_TO_CLAIM` -- 사고원인대분류 -> CLAIM
		FOREIGN KEY (
			`ACCI_DVSN` -- 사고종류
		)
		REFERENCES `insurance`.`CAUS_1` ( -- 사고원인대분류
			`ACCI_DVSN` -- 사고원인대분류
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_CAUS_2_TO_CLAIM` -- 사고원인소분류 -> CLAIM
		FOREIGN KEY (
			`CAUS_CODE` -- 사고원인코드
		)
		REFERENCES `insurance`.`CAUS_2` ( -- 사고원인소분류
			`CAUS_CODE` -- 사고원인코드
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_CAUS_3_TO_CLAIM` -- 사고원인세부특징 -> CLAIM
		FOREIGN KEY (
			`CAUS_CODE_DTAL` -- 사고원인세부
		)
		REFERENCES `insurance`.`CAUS_3` ( -- 사고원인세부특징
			`CAUS_CODE_DTAL` -- 사고원인세부
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_DMND_RESN_CODE_TO_CLAIM` -- 청구사유 -> CLAIM
		FOREIGN KEY (
			`DMND_RESN_CODE` -- 청구사유코드
		)
		REFERENCES `insurance`.`DMND_RESN_CODE` ( -- 청구사유
			`DMND_RESN_CODE` -- 청구사유코드
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_CAUS_2_TO_CLAIM2` -- 사고원인소분류 -> CLAIM2
		FOREIGN KEY (
			`RESL_CD1` -- 최종원인코드
		)
		REFERENCES `insurance`.`CAUS_2` ( -- 사고원인소분류
			`CAUS_CODE` -- 사고원인코드
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_LOCALE_TO_CLAIM` -- 지역 -> CLAIM
		FOREIGN KEY (
			`ACCI_HOSP_ADDR` -- 병원지역
		)
		REFERENCES `insurance`.`LOCALE` ( -- 지역
			`ACCI_HOSP_DIST` -- 지역코드
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_HOSP_SPEC_DVSN_TO_CLAIM` -- 병원종별구분 -> CLAIM
		FOREIGN KEY (
			`HOSP_SPEC_DVSN` -- 병원종별구분
		)
		REFERENCES `insurance`.`HOSP_SPEC_DVSN` ( -- 병원종별구분
			`HOSP_SPEC_DVSN` -- 병원종별구분
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_YN_TO_CLAIM2` -- YN -> CLAIM2
		FOREIGN KEY (
			`PMMI_DLNG_YN` -- 실손처리?
		)
		REFERENCES `insurance`.`YN` ( -- YN
			`YN` -- YN
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_YN_TO_CLAIM3` -- YN -> CLAIM3
		FOREIGN KEY (
			`HEED_HOSP_YN` -- 금감원 유의병원?
		)
		REFERENCES `insurance`.`YN` ( -- YN
			`YN` -- YN
		);

-- CLAIM
ALTER TABLE `insurance`.`CLAIM`
	ADD CONSTRAINT `FK_POLY_NO_TO_CLAIM` -- 임시 테이블 -> CLAIM
		FOREIGN KEY (
			`POLY_NO` -- 보험계약번호
		)
		REFERENCES `insurance`.`POLY_NO` ( -- 임시 테이블
			`POLY_NO` -- 보험계약번호
		);

-- CNTT
ALTER TABLE `insurance`.`CNTT`
	ADD CONSTRAINT `FK_CUST_TO_CNTT` -- CUST -> CNTT
		FOREIGN KEY (
			`CUST_ID` -- 고객번호
		)
		REFERENCES `insurance`.`CUST` ( -- CUST
			`CUST_ID` -- 고객번호
		);

-- CNTT
ALTER TABLE `insurance`.`CNTT`
	ADD CONSTRAINT `FK_FPINFO_TO_CNTT` -- FPINFO -> CNTT
		FOREIGN KEY (
			`CLLT_FP_PRNO` -- FP사번
		)
		REFERENCES `insurance`.`FPINFO` ( -- FPINFO
			`CLLT_FP_PRNO` -- FP사번
		);

-- CNTT
ALTER TABLE `insurance`.`CNTT`
	ADD CONSTRAINT `FK_CUST_ROLE_TO_CNTT` -- 고객역할코드 -> CNTT
		FOREIGN KEY (
			`CUST_ROLE` -- 고객역할코드
		)
		REFERENCES `insurance`.`CUST_ROLE` ( -- 고객역할코드
			`CUST_ROLE` -- 고객역할코드
		);

-- CNTT
ALTER TABLE `insurance`.`CNTT`
	ADD CONSTRAINT `FK_GOOD_CLSF_CDNM_TO_CNTT` -- 상품분류18종 -> CNTT
		FOREIGN KEY (
			`GOOD_CLSF_CDNM` -- 상품분류18종
		)
		REFERENCES `insurance`.`GOOD_CLSF_CDNM` ( -- 상품분류18종
			`GOOD_CLSF_CDNM` -- 상품분류18종
		);

-- CNTT
ALTER TABLE `insurance`.`CNTT`
	ADD CONSTRAINT `FK_SALE_CHNL_CODE_TO_CNTT` -- 판매채널코드 -> CNTT
		FOREIGN KEY (
			`SALE_CHNL_CODE` -- 판매채널코드
		)
		REFERENCES `insurance`.`SALE_CHNL_CODE` ( -- 판매채널코드
			`SALE_CHNL_CODE` -- 판매채널코드
		);

-- CNTT
ALTER TABLE `insurance`.`CNTT`
	ADD CONSTRAINT `FK_PAYM_CYCL_CODE_TO_CNTT` -- 납입주기 -> CNTT
		FOREIGN KEY (
			`PAYM_CYCL_CODE` -- 납입주기코드
		)
		REFERENCES `insurance`.`PAYM_CYCL_CODE` ( -- 납입주기
			`PAYM_CYCL_CODE` -- 납입주기코드
		);

-- CNTT
ALTER TABLE `insurance`.`CNTT`
	ADD CONSTRAINT `FK_CNTT_STAT_CODE_TO_CNTT` -- 계약상태 -> CNTT
		FOREIGN KEY (
			`CNTT_STAT_CODE` -- 계약상태코드
		)
		REFERENCES `insurance`.`CNTT_STAT_CODE` ( -- 계약상태
			`CNTT_STAT_CODE` -- 계약상태코드
		);

-- CNTT
ALTER TABLE `insurance`.`CNTT`
	ADD CONSTRAINT `FK_POLY_NO_TO_CNTT` -- 임시 테이블 -> CNTT
		FOREIGN KEY (
			`POLY_NO` -- 보험계약번호
		)
		REFERENCES `insurance`.`POLY_NO` ( -- 임시 테이블
			`POLY_NO` -- 보험계약번호
		);

-- FMLY
ALTER TABLE `insurance`.`FMLY`
	ADD CONSTRAINT `FK_CUST_TO_FMLY` -- CUST -> FMLY
		FOREIGN KEY (
			`CUST_ID` -- 고객번호
		)
		REFERENCES `insurance`.`CUST` ( -- CUST
			`CUST_ID` -- 고객번호
		);

-- FMLY
ALTER TABLE `insurance`.`FMLY`
	ADD CONSTRAINT `FK_CUST_TO_FMLY2` -- CUST -> FMLY2
		FOREIGN KEY (
			`ACCI_OCCP_GRP2` -- 가족고객번호
		)
		REFERENCES `insurance`.`CUST` ( -- CUST
			`CUST_ID` -- 고객번호
		);

-- FMLY
ALTER TABLE `insurance`.`FMLY`
	ADD CONSTRAINT `FK_FMLY_RELN_CODE_TO_FMLY` -- 가족관계 -> FMLY
		FOREIGN KEY (
			`FMLY_RELN_CODE` -- 가족관계코드
		)
		REFERENCES `insurance`.`FMLY_RELN_CODE` ( -- 가족관계
			`FMLY_RELN_CODE` -- 가족관계코드
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_DIVIDED_SET_TO_CUST` -- 데이터구분 -> CUST
		FOREIGN KEY (
			`DIVIDED_SET` -- 학습데이터?
		)
		REFERENCES `insurance`.`DIVIDED_SET` ( -- 데이터구분
			`DIVIDED_SET` -- 학습데이터?
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_SIU_CUST_YN_TO_CUST` -- 임시 테이블2 -> CUST
		FOREIGN KEY (
			`SIU_CUST_YN` -- 보험사기자?
		)
		REFERENCES `insurance`.`SIU_CUST_YN` ( -- 임시 테이블2
			`SIU_CUST_YN` -- 보험사기자?
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_SEX_TO_CUST` -- 남/여? -> CUST
		FOREIGN KEY (
			`SEX` -- 성별
		)
		REFERENCES `insurance`.`SEX` ( -- 남/여?
			`SEX` -- 성별
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_RESI_TYPE_CODE_TO_CUST` -- 거주형태 -> CUST
		FOREIGN KEY (
			`RESI_TYPE_CODE` -- 거주형태
		)
		REFERENCES `insurance`.`RESI_TYPE_CODE` ( -- 거주형태
			`RESI_TYPE_CODE` -- 거주형태
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_YN_TO_CUST` -- YN -> CUST
		FOREIGN KEY (
			`FP_CAREER` -- FP경력자?
		)
		REFERENCES `insurance`.`YN` ( -- YN
			`YN` -- YN
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_LOCALE_TO_CUST` -- 지역 -> CUST
		FOREIGN KEY (
			`CTPR` -- 거주시도
		)
		REFERENCES `insurance`.`LOCALE` ( -- 지역
			`ACCI_HOSP_DIST` -- 지역코드
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_JOB8_TO_CUST` -- 직업대분류(8종) -> CUST
		FOREIGN KEY (
			`OCCP_GRP1` -- 직업대분류8
		)
		REFERENCES `insurance`.`JOB8` ( -- 직업대분류(8종)
			`ACCI_OCCP_GRP1` -- 직업대분류8
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_JOB25_TO_CUST` -- 직업소분류(25종) -> CUST
		FOREIGN KEY (
			`OCCP_GRP2` -- 직업소분류25
		)
		REFERENCES `insurance`.`JOB25` ( -- 직업소분류(25종)
			`ACCI_OCCP_GRP2` -- 직업소분류25
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_YN_TO_CUST2` -- YN -> CUST2
		FOREIGN KEY (
			`WEDD_YN` -- 결혼?
		)
		REFERENCES `insurance`.`YN` ( -- YN
			`YN` -- YN
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_JOB25_TO_CUST2` -- 직업소분류(25종) -> CUST2
		FOREIGN KEY (
			`MATE_OCCP_GRP2` -- 배우자직업8
		)
		REFERENCES `insurance`.`JOB25` ( -- 직업소분류(25종)
			`ACCI_OCCP_GRP2` -- 직업소분류25
		);

-- CUST
ALTER TABLE `insurance`.`CUST`
	ADD CONSTRAINT `FK_JOB8_TO_CUST2` -- 직업대분류(8종) -> CUST2
		FOREIGN KEY (
			`MATE_OCCP_GRP1` -- 배우자직업25
		)
		REFERENCES `insurance`.`JOB8` ( -- 직업대분류(8종)
			`ACCI_OCCP_GRP1` -- 직업대분류8
		);

-- FPINFO
ALTER TABLE `insurance`.`FPINFO`
	ADD CONSTRAINT `FK_INCB_DVSN_TO_FPINFO` -- FP고용형태 -> FPINFO
		FOREIGN KEY (
			`INCB_DVSN` -- FP고용형태
		)
		REFERENCES `insurance`.`INCB_DVSN` ( -- FP고용형태
			`INCB_DVSN` -- FP고용형태
		);

-- FPINFO
ALTER TABLE `insurance`.`FPINFO`
	ADD CONSTRAINT `FK_BEFO_JOB_TO_FPINFO` -- FP이전직업 -> FPINFO
		FOREIGN KEY (
			`BEFO_JOB` -- FP이전직업
		)
		REFERENCES `insurance`.`BEFO_JOB` ( -- FP이전직업
			`BEFO_JOB` -- FP이전직업
		);

-- FPINFO
ALTER TABLE `insurance`.`FPINFO`
	ADD CONSTRAINT `FK_EDGB_TO_FPINFO` -- FP최종학력 -> FPINFO
		FOREIGN KEY (
			`EDGB` -- FP최종학력
		)
		REFERENCES `insurance`.`EDGB` ( -- FP최종학력
			`EDGB` -- FP최종학력
		);