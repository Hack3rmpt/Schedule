--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4
-- Dumped by pg_dump version 15.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: course; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.course (
    id integer NOT NULL,
    number integer NOT NULL,
    specialization_id integer NOT NULL
);


ALTER TABLE public.course OWNER TO postgres;

--
-- Name: course_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.course_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.course_id_seq OWNER TO postgres;

--
-- Name: course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.course_id_seq OWNED BY public.course.id;


--
-- Name: direction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.direction (
    id integer NOT NULL,
    code character varying(20) NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.direction OWNER TO postgres;

--
-- Name: direction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.direction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.direction_id_seq OWNER TO postgres;

--
-- Name: direction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.direction_id_seq OWNED BY public.direction.id;


--
-- Name: exam; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exam (
    id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    duration integer,
    subject_id integer NOT NULL,
    group_id integer NOT NULL,
    teacher_id integer NOT NULL,
    room_id integer NOT NULL
);


ALTER TABLE public.exam OWNER TO postgres;

--
-- Name: exam_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exam_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exam_id_seq OWNER TO postgres;

--
-- Name: exam_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exam_id_seq OWNED BY public.exam.id;


--
-- Name: room; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.room (
    id integer NOT NULL,
    number character varying(10) NOT NULL,
    capacity integer NOT NULL,
    type character varying(20),
    building character varying(50)
);


ALTER TABLE public.room OWNER TO postgres;

--
-- Name: room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.room_id_seq OWNER TO postgres;

--
-- Name: room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.room_id_seq OWNED BY public.room.id;


--
-- Name: schedule_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schedule_log (
    id integer NOT NULL,
    action character varying(255) NOT NULL,
    "timestamp" timestamp without time zone,
    direction_id integer NOT NULL,
    user_id integer
);


ALTER TABLE public.schedule_log OWNER TO postgres;

--
-- Name: schedule_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.schedule_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schedule_log_id_seq OWNER TO postgres;

--
-- Name: schedule_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.schedule_log_id_seq OWNED BY public.schedule_log.id;


--
-- Name: schedule_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schedule_settings (
    id integer NOT NULL,
    direction_id integer NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    max_exams_per_day integer,
    min_days_between_exams integer
);


ALTER TABLE public.schedule_settings OWNER TO postgres;

--
-- Name: schedule_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.schedule_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schedule_settings_id_seq OWNER TO postgres;

--
-- Name: schedule_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.schedule_settings_id_seq OWNED BY public.schedule_settings.id;


--
-- Name: specialization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.specialization (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    direction_id integer NOT NULL
);


ALTER TABLE public.specialization OWNER TO postgres;

--
-- Name: specialization_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.specialization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.specialization_id_seq OWNER TO postgres;

--
-- Name: specialization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.specialization_id_seq OWNED BY public.specialization.id;


--
-- Name: student_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student_group (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    course_id integer NOT NULL
);


ALTER TABLE public.student_group OWNER TO postgres;

--
-- Name: student_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_group_id_seq OWNER TO postgres;

--
-- Name: student_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_group_id_seq OWNED BY public.student_group.id;


--
-- Name: subject; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subject (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    assessment_type character varying(100) NOT NULL,
    course_id integer NOT NULL
);


ALTER TABLE public.subject OWNER TO postgres;

--
-- Name: subject_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subject_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subject_id_seq OWNER TO postgres;

--
-- Name: subject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subject_id_seq OWNED BY public.subject.id;


--
-- Name: teacher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teacher (
    id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    patronymic character varying(50),
    email character varying(120) NOT NULL
);


ALTER TABLE public.teacher OWNER TO postgres;

--
-- Name: teacher_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teacher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teacher_id_seq OWNER TO postgres;

--
-- Name: teacher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teacher_id_seq OWNED BY public.teacher.id;


--
-- Name: teacher_subject; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teacher_subject (
    teacher_id integer NOT NULL,
    subject_id integer NOT NULL
);


ALTER TABLE public.teacher_subject OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(64) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(128) NOT NULL,
    role character varying(20) NOT NULL,
    is_active boolean,
    created_at timestamp without time zone
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: course id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course ALTER COLUMN id SET DEFAULT nextval('public.course_id_seq'::regclass);


--
-- Name: direction id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.direction ALTER COLUMN id SET DEFAULT nextval('public.direction_id_seq'::regclass);


--
-- Name: exam id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam ALTER COLUMN id SET DEFAULT nextval('public.exam_id_seq'::regclass);


--
-- Name: room id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room ALTER COLUMN id SET DEFAULT nextval('public.room_id_seq'::regclass);


--
-- Name: schedule_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule_log ALTER COLUMN id SET DEFAULT nextval('public.schedule_log_id_seq'::regclass);


--
-- Name: schedule_settings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule_settings ALTER COLUMN id SET DEFAULT nextval('public.schedule_settings_id_seq'::regclass);


--
-- Name: specialization id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialization ALTER COLUMN id SET DEFAULT nextval('public.specialization_id_seq'::regclass);


--
-- Name: student_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_group ALTER COLUMN id SET DEFAULT nextval('public.student_group_id_seq'::regclass);


--
-- Name: subject id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject ALTER COLUMN id SET DEFAULT nextval('public.subject_id_seq'::regclass);


--
-- Name: teacher id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher ALTER COLUMN id SET DEFAULT nextval('public.teacher_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: course; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.course (id, number, specialization_id) FROM stdin;
1	2	5
2	3	5
\.


--
-- Data for Name: direction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.direction (id, code, name) FROM stdin;
8	09.02.07	Информационные системы
6	09.02.09	Веб-разработка
4	40.02.04	Юриспруденция
13	фев	фыв
\.


--
-- Data for Name: exam; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exam (id, datetime, duration, subject_id, group_id, teacher_id, room_id) FROM stdin;
15	2025-04-08 10:10:00	90	3	8	3	10
16	2025-04-21 08:30:00	90	9	7	5	4
17	2025-04-21 10:10:00	90	7	8	9	4
18	2025-04-21 12:00:00	90	8	13	7	4
19	2025-04-22 10:10:00	90	3	11	3	12
20	2025-04-22 08:30:00	90	3	13	3	10
21	2025-04-23 08:30:00	90	9	7	5	4
22	2025-04-23 12:00:00	90	8	8	7	4
23	2025-04-23 10:10:00	90	7	11	9	4
24	2025-04-24 12:00:00	90	3	7	3	12
25	2025-04-25 08:30:00	90	7	7	9	4
26	2025-04-25 12:00:00	90	9	8	5	4
27	2025-04-25 10:10:00	90	4	11	4	4
\.


--
-- Data for Name: room; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.room (id, number, capacity, type, building) FROM stdin;
4	122	12	lecture	Корпус на ул. Нахимовский проспект 21
5	100	30	practice	Корпус на ул. Нежинской 7
6	101	30	lab	Корпус на ул. Нежинской 7
7	102	30	lab	Корпус на ул. Нежинской 7
8	200	30	lab	Корпус на ул. Нежинской 7
9	201	30	practice	Корпус на ул. Нежинской 7
10	202	30	practice	Корпус на ул. Нежинской 7
11	330	30	lab	Корпус на ул. Нежинской 7
12	320	30	practice	Корпус на ул. Нежинской 7
\.


--
-- Data for Name: schedule_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.schedule_log (id, action, "timestamp", direction_id, user_id) FROM stdin;
\.


--
-- Data for Name: schedule_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.schedule_settings (id, direction_id, start_date, end_date, max_exams_per_day, min_days_between_exams) FROM stdin;
\.


--
-- Data for Name: specialization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.specialization (id, name, direction_id) FROM stdin;
4	фывфывфыв	4
3	test	4
7	Веб дизайн	6
5	Программист	8
6	Тестировщик	8
\.


--
-- Data for Name: student_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student_group (id, name, course_id) FROM stdin;
7	П50-2-22	2
8	П50-1-22	2
11	П50-3-22	2
13	П50-4-22	2
14	П50-1-23	1
15	П50-2-23	1
16	П50-3-23	1
17	П50-4-24	1
\.


--
-- Data for Name: subject; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subject (id, name, assessment_type, course_id) FROM stdin;
1	ОАИП	Экзамен	1
2	Дискретаня математика	Зачет	1
3	Программирование	Экзамен	2
4	Математическое моделирование	Экзамен	2
5	Операционные системы	Экзамен	2
6	Философия	Зачет	2
7	Тестирование	Экзамен	2
8	Обеспечение качества	Экзамен	2
9	Мобильная разработка	Экзамен	2
10	Разработка мобильных приложенний	Зачет	1
\.


--
-- Data for Name: teacher; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teacher (id, first_name, last_name, patronymic, email) FROM stdin;
9	Елена	Кузнецова	Анатольевна	elena@mail.com
11	Роман	Сазонов	Валериевна	dementi_24@example.org
12	Венедикт	Колобов	Харлампович	gromovstanimir@example.net
13	Агата	Иванов	Васильевна	antonina12@example.com
14	Евсей	Лебедева	Даниилович	titovaleksandr@example.com
15	Игнатий	Алексеев	Кузьминична	irakli12@example.com
16	Матвей	Лукина	Захарьевич	aksenovaaleksandra@example.org
17	Олимпий	Кузнецова	Харитоновна	spartak29@example.com
18	Емельян	Лукина	Феликсовна	komarovluchezar@example.net
8	Максим	Брагин	Жанович	mina1992@example.com
19	Фаина	Сазонов	Александровна	volkovnikola@example.com
20	Мина	Ершов	Феликсовна	ereme_2020@example.net
3	Силантий	Воронцов	Филиппович	provdrozdov@example.org
21	Кондрат	Журавлев	Григорьевич	savva1993@example.org
7	Клавдий	Кулагин	Фокич	ekozlov@example.org
22	Ульяна	Блинова	Игоревич	fadeevanikita@example.com
4	Моисей	Смирнова	Богдановна	apollinari_2005@example.org
23	Лидия	Шестаков	Арсенович	kirill_2012@example.com
24	Тимофей	Агафонова	Матвеевич	sigizmund1989@example.net
25	Якуб	Емельянова	Адамович	timur10@example.org
26	Афанасий	Ефимов	Гертрудович	shestakovveniamin@example.net
27	Милан	Рыбаков	Игнатович	moise_2012@example.org
28	Лев	Лебедев	Никифоровна	ykosheleva@example.net
29	Владимир	Куликова	Авдеевич	mechislav92@example.net
6	Платон	Сысоева	Устинович	zosima_21@example.org
5	Сигизмунд	Емельянова	Георгиевич	evfrosinija93@example.net
30	Фадей	Муравьева	Иларионович	evgenija06@example.org
31	Василисаa	Жуков	Тимурович	orehovjuli@example.net
\.


--
-- Data for Name: teacher_subject; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teacher_subject (teacher_id, subject_id) FROM stdin;
4	4
3	3
4	6
9	7
7	8
5	9
3	10
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, email, password_hash, role, is_active, created_at) FROM stdin;
1	admin	admin@example.com	$2b$12$1/csNG7APa69Osj3.DD2xutBIai03EyFrC93/Qpa2nx5rx.CcXsUW	admin	t	2025-03-17 14:23:22.415209
3	Dima	Dima@mail.ru	$2b$12$da9Jy/84ovQICR4UH4RINe5QiiJa5IzbWH59AsBdJtavBbbYJWLiW	worker	t	2025-03-19 09:25:28.551864
\.


--
-- Name: course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.course_id_seq', 2, true);


--
-- Name: direction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.direction_id_seq', 13, true);


--
-- Name: exam_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exam_id_seq', 27, true);


--
-- Name: room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.room_id_seq', 13, true);


--
-- Name: schedule_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.schedule_log_id_seq', 1, false);


--
-- Name: schedule_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.schedule_settings_id_seq', 1, false);


--
-- Name: specialization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.specialization_id_seq', 7, true);


--
-- Name: student_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_group_id_seq', 17, true);


--
-- Name: subject_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subject_id_seq', 10, true);


--
-- Name: teacher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teacher_id_seq', 36, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 3, true);


--
-- Name: course course_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_pkey PRIMARY KEY (id);


--
-- Name: direction direction_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.direction
    ADD CONSTRAINT direction_code_key UNIQUE (code);


--
-- Name: direction direction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.direction
    ADD CONSTRAINT direction_pkey PRIMARY KEY (id);


--
-- Name: exam exam_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_pkey PRIMARY KEY (id);


--
-- Name: room room_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_number_key UNIQUE (number);


--
-- Name: room room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id);


--
-- Name: schedule_log schedule_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule_log
    ADD CONSTRAINT schedule_log_pkey PRIMARY KEY (id);


--
-- Name: schedule_settings schedule_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule_settings
    ADD CONSTRAINT schedule_settings_pkey PRIMARY KEY (id);


--
-- Name: specialization specialization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialization
    ADD CONSTRAINT specialization_pkey PRIMARY KEY (id);


--
-- Name: student_group student_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_group
    ADD CONSTRAINT student_group_name_key UNIQUE (name);


--
-- Name: student_group student_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_group
    ADD CONSTRAINT student_group_pkey PRIMARY KEY (id);


--
-- Name: subject subject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT subject_pkey PRIMARY KEY (id);


--
-- Name: teacher teacher_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT teacher_email_key UNIQUE (email);


--
-- Name: teacher teacher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT teacher_pkey PRIMARY KEY (id);


--
-- Name: teacher_subject teacher_subject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher_subject
    ADD CONSTRAINT teacher_subject_pkey PRIMARY KEY (teacher_id, subject_id);


--
-- Name: subject unique_subject_name_per_course; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT unique_subject_name_per_course UNIQUE (name, course_id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: course course_specialization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_specialization_id_fkey FOREIGN KEY (specialization_id) REFERENCES public.specialization(id);


--
-- Name: exam exam_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.student_group(id);


--
-- Name: exam exam_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id);


--
-- Name: exam exam_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subject(id);


--
-- Name: exam exam_teacher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.teacher(id);


--
-- Name: schedule_log schedule_log_direction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule_log
    ADD CONSTRAINT schedule_log_direction_id_fkey FOREIGN KEY (direction_id) REFERENCES public.direction(id);


--
-- Name: schedule_log schedule_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule_log
    ADD CONSTRAINT schedule_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: schedule_settings schedule_settings_direction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule_settings
    ADD CONSTRAINT schedule_settings_direction_id_fkey FOREIGN KEY (direction_id) REFERENCES public.direction(id);


--
-- Name: specialization specialization_direction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialization
    ADD CONSTRAINT specialization_direction_id_fkey FOREIGN KEY (direction_id) REFERENCES public.direction(id);


--
-- Name: student_group student_group_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_group
    ADD CONSTRAINT student_group_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id);


--
-- Name: subject subject_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT subject_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id);


--
-- Name: teacher_subject teacher_subject_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher_subject
    ADD CONSTRAINT teacher_subject_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subject(id);


--
-- Name: teacher_subject teacher_subject_teacher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher_subject
    ADD CONSTRAINT teacher_subject_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.teacher(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

