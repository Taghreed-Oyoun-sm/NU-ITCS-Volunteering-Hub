from backend.db_connection import SessionLocal

from backend.students.db_operations import create_user
from backend.students.dtos import UserCreate

from backend.posts.db_operations import (
    create_post,
    search_posts_by_tag,
    find_suitable_students,
    create_comment  # make sure you have this function
)
from backend.posts.dtos import PostCreate, CommentCreate  # assuming you have a DTO for comments


def run():
    db = SessionLocal()

    # ---------------- CREATE STUDENT ----------------
    student = create_user(
        db,
        UserCreate(
            student_id=231000096,
            name="Taghreed Oyoun",
            email="taghreed@nu.edu.eg",
            password="123456",
            year="Junior",
            track="CS",
            cgpa=3.9,
            research_skills=False,
            jta_skills=False,
            strength_areas=[
                "Logic Design",
                "Differential Equations"
            ]
        )
    )
    print("Student created:", student.name, student.strength_areas)

    # ---------------- CREATE POST ----------------
    post = create_post(
        db,
        PostCreate(
            student_id=student.student_id,
            title="Logic Design Help",
            content="Need help with Karnaugh Maps",
            tags=["Logic Design"]
        )
    )
    print("Post created:", post.title, post.tags)

    # ---------------- CREATE COMMENT ----------------
    comment = create_comment(
        db,
        CommentCreate(
            post_id=post.post_id,
            student_id=student.student_id,
            content="I can help you with this!"
        )
    )
    print("Comment added:", comment.content)

    # ---------------- CREATE REPLY ----------------
    reply = create_comment(
        db,
        CommentCreate(
            post_id=post.post_id,
            student_id=student.student_id,
            content="Thanks! That would be great.",
            parent_id=comment.id  # reply to the first comment
        )
    )
    print("Reply added:", reply.content, "(reply to comment ID:", comment.id, ")")

    # ---------------- SEARCH BY TAG ----------------
    posts = search_posts_by_tag(db, "Logic Design")
    print("\nPosts with tag 'Logic Design':")
    for p in posts:
        print("-", p.title)

        # print comments and replies for this post
        for c in p.comments:
            print("  Comment:", c.content)
            for r in c.replies:
                print("    Reply:", r.content)

    # ---------------- MATCH STUDENTS ----------------
    matched_students = find_suitable_students(db, ["Logic Design"])
    print("\nStudents suitable for Logic Design:")
    for s in matched_students:
        print("-", s.name, "(ID:", s.student_id, ")")

    db.close()


if __name__ == "__main__":
    run()
