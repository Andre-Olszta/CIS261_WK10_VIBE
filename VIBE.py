"""Student Grade Calculator."""

import csv
import os


DATA_FILE = "student_grades.txt"


def calculate_grade(average: float) -> str:
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def create_student(name: str, student_id: str, test1: float, test2: float, test3: float) -> dict:
	average = (test1 + test2 + test3) / 3
	return {
		"name": name,
		"id": student_id,
		"test1": test1,
		"test2": test2,
		"test3": test3,
		"average": average,
		"grade": calculate_grade(average),
	}


def get_score(prompt: str) -> float:
	"""Read a test score between 0 and 100."""
	while True:
		try:
			score = float(input(prompt))
			if 0 <= score <= 100:
				return score
			print("Please enter a score from 0 to 100.")
		except ValueError:
			print("Please enter a valid number.")


def save_students(students: list[dict], filename: str = DATA_FILE) -> None:
	"""Save records in a CSV format that can be read back safely."""
	try:
		with open(filename, "w", newline="", encoding="utf-8") as file:
			writer = csv.writer(file, delimiter="|", lineterminator="\n")
			for student in students:
				writer.writerow([
					student[key]
					for key in ["name", "id", "test1", "test2", "test3", "average", "grade"]
				])
	except OSError as error:
		print(f"Could not save {filename}: {error}")


def load_students(filename: str = DATA_FILE) -> list[dict]:
	"""Load saved records, ignoring incomplete or invalid rows."""
	if not os.path.exists(filename):
		return []

	students = []
	try:
		with open(filename, newline="", encoding="utf-8") as file:
			for row in csv.reader(file, delimiter="|"):
				if len(row) != 7 or row[0].strip().casefold() == "name":
					continue
				try:
					students.append(create_student(
						row[0].strip(),
						row[1].strip(),
						float(row[2]),
						float(row[3]),
						float(row[4]),
					))
				except (TypeError, ValueError):
					continue
	except OSError as error:
		print(f"Could not load {filename}: {error}")
	return students


def add_student(students: list[dict]) -> None:
	print("\nAdd Student")
	name = input("Student name: ").strip()
	student_id = input("Student ID: ").strip()
	test1 = get_score("Test 1 score: ")
	test2 = get_score("Test 2 score: ")
	test3 = get_score("Test 3 score: ")
	students.append(create_student(name, student_id, test1, test2, test3))
	print("Student added.")


def display_students(students: list[dict]) -> None:
	if not students:
		print("\nNo student records found.")
		return

	print("\nStudent Records")
	print("-" * 86)
	print(f"{'Name':<22} {'ID':<14} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>9} {'Grade':>6}")
	print("-" * 86)
	for student in students:
		print(
			f"{student['name']:<22.22} {student['id']:<14.14} "
			f"{student['test1']:>8.2f} {student['test2']:>8.2f} {student['test3']:>8.2f} "
			f"{student['average']:>9.2f} {student['grade']:>6}"
		)
	print("-" * 86)


def display_statistics(students: list[dict]) -> None:
	if not students:
		print("\nNo student records found.")
		return

	averages = [student["average"] for student in students]
	highest = max(students, key=lambda student: student["average"])
	lowest = min(students, key=lambda student: student["average"])
	print("\nClass Statistics")
	print(f"Highest average: {highest['average']:.2f} ({highest['name']})")
	print(f"Lowest average:  {lowest['average']:.2f} ({lowest['name']})")
	print(f"Class average:    {sum(averages) / len(averages):.2f}")


def search_student(students: list[dict]) -> None:
	search_name = input("\nEnter a name to search: ").strip().casefold()
	matches = [student for student in students if search_name in student["name"].casefold()]
	if matches:
		display_students(matches)
	else:
		print("No matching students found.")


def show_menu() -> str:
	print("\nStudent Grade Calculator")
	print("1. Add a student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search by name")
	print("5. Save records")
	print("Press ESC then Enter to exit")
	return input("Select an option: ").strip()


def main() -> None:
	students: list[dict] = load_students()
	if students:
		print(f"Loaded {len(students)} student record(s) from {DATA_FILE}.")

	while True:
		choice = show_menu()
		if choice == "\x1b":
			save_students(students)
			print(f"Records saved to {DATA_FILE}. Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		elif choice == "5":
			save_students(students)
			print(f"Records saved to {DATA_FILE}.")
		else:
			print("Please choose 1-5, or press ESC to exit.")


if __name__ == "__main__":
	main()
