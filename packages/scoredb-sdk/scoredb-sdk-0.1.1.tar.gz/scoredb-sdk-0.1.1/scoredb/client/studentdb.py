from typing import Union, List

from requests import Session

from ._baseapi import BaseAPI
from ._pagination import Pagination
from ..models import GradeSummary, Grade, ClassSummary, Class, StudentSummary, Student


class StudentDBAPI(BaseAPI):

    def __init__(self, session: Session, base_url: str):
        super().__init__(session, base_url + '/studentdb')

    def get_all_grades(self):
        result = self.request('GET', '/grades')
        return [GradeSummary(**grade) for grade in result]

    def get_grade_details(self, grade: Union[GradeSummary, str]):
        grade_id: str = grade.id if type(grade) == GradeSummary else grade
        result = self.request('GET', f'/grades/{grade_id}')
        result['classes'] = [ClassSummary(**class_) for class_ in result['classes']]
        return Grade(**result)

    def get_class_details(self, class_: Union[ClassSummary, str]):
        class_id: str = class_.id if type(class_) == ClassSummary else class_
        result = self.request('GET', f'/classes/{class_id}')
        result['students'] = [StudentSummary(**student) for student in result['students']]
        return Class(**result)

    def get_student_details(self, student: Union[StudentSummary, str], with_photos=False):
        student_id: str = student.id if type(student) == StudentSummary else student
        result = self.request('GET', f'/students/{student_id}', params={
            'photos': str(with_photos).lower()
        })
        return Student(**result)

    def get_student_photos(self, student: Union[Student, StudentSummary, str]) -> List[str]:
        if type(student) == Student:
            if student.photos is not None:
                return student.photos
            else:
                student = student.id
        return self.get_student_details(student, True).photos

    def search_student(self, query: str, page: int = 1) -> Pagination[StudentSummary]:
        if not query:
            raise ValueError('Empty query.')
        result = self.request('GET', '/search', params={
            'query': query,
            'page': page
        })

        result['data'] = [StudentSummary(**student) for student in result['data']]

        def switch_page_fn(new_page: int):
            return self.search_student(query, new_page)

        return Pagination(**result, switch_page_fn=switch_page_fn)
