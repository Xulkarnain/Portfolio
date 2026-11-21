
from app.core.exceptions import (
    ResourceNotFoundException,
    DuplicateResourceException,
    InvalidReferenceException,
    PortfolioOwnerNotFoundException,
    InvalidInputException,
    
)
from app.repositories.project import ProjectRepository
from app.schemas.project import AdminProjectCreate ,AdminProjectUpdate


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def get_public_projects(self):
        return self.repository.get_published_projects()

    def get_project(self, project_id: int):
        project = self.repository.get_by_id(project_id)

        if project is None:
            raise ResourceNotFoundException("Project", project_id)

        return project

    def get_all_projects(self):
        return self.repository.get_all_projects()

    def create_project(self, project_data: AdminProjectCreate):
        try:
            # 1. Resolve the portfolio owner.
            owner = self.repository.get_portfolio_owner()

            if owner is None:
                raise PortfolioOwnerNotFoundException()

            # 2. Check slug uniqueness.
            existing_project = self.repository.get_by_slug(
                project_data.slug
            )

            if existing_project is not None:
                raise DuplicateResourceException(
                    "Project",
                    "slug",
                    project_data.slug,
                )

            
            # 3. Validate duplicate skill IDs.
            skill_ids = project_data.skill_ids

            if len(skill_ids) != len(set(skill_ids)):
                raise InvalidInputException(
                    "Duplicate skill IDs are not allowed"
                )

            # 4. Retrieve and validate requested skills.
            skills = self.repository.get_skills_by_ids(skill_ids)

            found_skill_ids = {skill.id for skill in skills}

            invalid_skill_ids = [
                skill_id
                for skill_id in skill_ids
                if skill_id not in found_skill_ids
            ]

            if invalid_skill_ids:
                raise InvalidReferenceException(
                    "Skill",
                    invalid_skill_ids,
                )

            # 5. Validate project categories.
            allowed_categories = {"ai", "backend", "data"}

            invalid_categories = [
                category
                for category in project_data.categories
                if category not in allowed_categories
            ]

            if invalid_categories:
                raise InvalidInputException(
                    f"Invalid project categories: {invalid_categories}"
                )

            if len(project_data.categories) != len(set(project_data.categories)):
                raise InvalidInputException(
                    "Duplicate project categories are not allowed"
                )

            # 6. Separate relationships from project columns.
            project_fields = project_data.model_dump(
                mode="json",
                exclude={"categories", "skill_ids"}
            )

            # 7. Create the project and its relationships.
            project = self.repository.create(
                project_data=project_fields,
                owner_id=owner.id,
                skills=skills,
                categories=project_data.categories,
            )

            # 8. Commit the transaction.
            self.repository.db.commit()

            # Reload with relationships after commit.
            return self.repository.get_by_id(project.id)

        except Exception:
            self.repository.db.rollback()
            raise

        
    def update_project(
        self,
        project_id: int,
        project_data: AdminProjectUpdate,
    ):
        try:
            # 1. Retrieve the existing project.
            project = self.repository.get_by_id(project_id)

            if project is None:
                raise ResourceNotFoundException("Project", project_id)

            # 2. Check whether another project uses the requested slug.
            existing_project = self.repository.get_by_slug(
                project_data.slug
            )

            if (
                existing_project is not None
                and existing_project.id != project_id
            ):
                raise DuplicateResourceException(
                    "Project",
                    "slug",
                    project_data.slug,
                )

            # 3. Validate duplicate skill IDs.
            skill_ids = project_data.skill_ids

            if len(skill_ids) != len(set(skill_ids)):
                raise InvalidInputException(
                    "Duplicate skill IDs are not allowed"
                )

            # 4. Retrieve and validate skills.
            skills = self.repository.get_skills_by_ids(skill_ids)

            found_skill_ids = {skill.id for skill in skills}

            invalid_skill_ids = [
                skill_id
                for skill_id in skill_ids
                if skill_id not in found_skill_ids
            ]

            if invalid_skill_ids:
                raise InvalidReferenceException(
                    "Skill",
                    invalid_skill_ids,
                )

            # 5. Validate categories.
            allowed_categories = {"ai", "backend", "data"}

            invalid_categories = [
                category
                for category in project_data.categories
                if category not in allowed_categories
            ]

            if invalid_categories:
                raise InvalidInputException(
                    f"Invalid project categories: {invalid_categories}"
                )

            if len(project_data.categories) != len(set(project_data.categories)):
                raise InvalidInputException(
                    "Duplicate project categories are not allowed"
                )

            # 6. Separate project columns from relationships.
            project_fields = project_data.model_dump(
                mode="json",
                exclude={"categories", "skill_ids"},
            )

            # 7. Update project and relationships.
            updated_project = self.repository.update(
                project=project,
                project_data=project_fields,
                skills=skills,
                categories=project_data.categories,
            )

            # 8. Commit transaction.
            self.repository.db.commit()

            return self.repository.get_by_id(updated_project.id)

        except Exception:
            self.repository.db.rollback()
            raise
