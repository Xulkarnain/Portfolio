from sqlalchemy import inspect
from sqlalchemy.dialects import postgresql

from app.database.connection import engine
from app.database.base import Base

# Import every model so all tables are registered in Base.metadata.
from app.models import (
    User,
    Project,
    SkillCategory,
    Skill,
    ProjectSkill,
    Experience,
    ExperienceSkill,
    Education,
    Certification,
    Post,
    Resume,
    ContactMessage,
    VisitorLog,
    SyncLog,
)


inspector = inspect(engine)

db_tables = set(inspector.get_table_names())
orm_tables = set(Base.metadata.tables.keys())


print("=" * 70)
print("ORM ↔ PostgreSQL SCHEMA AUDIT")
print("=" * 70)


# ======================================================================
# TABLE AUDIT
# ======================================================================

print("\nDATABASE TABLES")
print("-" * 70)

for table in sorted(db_tables):
    print(table)


print("\nORM TABLES")
print("-" * 70)

for table in sorted(orm_tables):
    print(table)


print("\nTABLE COMPARISON")
print("-" * 70)

missing_in_orm = db_tables - orm_tables
missing_in_db = orm_tables - db_tables

if not missing_in_orm:
    print("PASS: No PostgreSQL tables are missing from ORM metadata.")
else:
    print("FAIL: Tables missing in ORM:")
    for table in sorted(missing_in_orm):
        print(f"  - {table}")


if not missing_in_db:
    print("PASS: No ORM tables are missing from PostgreSQL.")
else:
    print("FAIL: Tables missing in PostgreSQL:")
    for table in sorted(missing_in_db):
        print(f"  - {table}")


# ======================================================================
# COLUMN AUDIT
# ======================================================================

print("\nCOLUMN COMPARISON")
print("-" * 70)

common_tables = sorted(db_tables & orm_tables)


for table_name in common_tables:

    db_columns = {
        column["name"]: column
        for column in inspector.get_columns(table_name)
    }

    orm_table = Base.metadata.tables[table_name]

    db_column_names = set(db_columns.keys())
    orm_column_names = {
        column.name
        for column in orm_table.columns
    }

    missing_in_orm = db_column_names - orm_column_names
    missing_in_db = orm_column_names - db_column_names

    column_mismatches = []

    # --------------------------------------------------------------
    # Check missing columns
    # --------------------------------------------------------------

    if missing_in_orm:
        column_mismatches.append(
            (
                "MISSING_IN_ORM",
                sorted(missing_in_orm),
            )
        )

    if missing_in_db:
        column_mismatches.append(
            (
                "MISSING_IN_POSTGRESQL",
                sorted(missing_in_db),
            )
        )

    # --------------------------------------------------------------
    # Compare common columns
    # --------------------------------------------------------------

    for column_name in sorted(
        db_column_names & orm_column_names
    ):

        db_column = db_columns[column_name]
        orm_column = orm_table.columns[column_name]

        db_type_obj = db_column["type"]
        orm_type_obj = orm_column.type

        db_type = str(db_type_obj)

        # Compile SQLAlchemy type using PostgreSQL dialect.
        orm_type = str(
            orm_type_obj.compile(
                dialect=postgresql.dialect()
            )
        )

        db_timezone = getattr(
            db_type_obj,
            "timezone",
            None,
        )

        orm_timezone = getattr(
            orm_type_obj,
            "timezone",
            None,
        )

        nullable_match = (
            db_column["nullable"]
            == orm_column.nullable
        )

        # ----------------------------------------------------------
        # PostgreSQL-aware type comparison
        # ----------------------------------------------------------

        if isinstance(
            db_type_obj,
            postgresql.TIMESTAMP,
        ):

            type_match = (
                isinstance(
                    orm_type_obj,
                    postgresql.TIMESTAMP,
                )
                and db_timezone == orm_timezone
            )

        else:

            type_match = (
                type(db_type_obj).__name__
                == type(orm_type_obj).__name__
            )

        # ----------------------------------------------------------
        # Store differences instead of printing matches
        # ----------------------------------------------------------

        if not type_match or not nullable_match:

            column_mismatches.append(
                (
                    "COLUMN_DIFFERENCE",
                    column_name,
                    type_match,
                    nullable_match,
                    db_type,
                    orm_type,
                    db_timezone,
                    orm_timezone,
                    db_column["nullable"],
                    orm_column.nullable,
                )
            )

    # --------------------------------------------------------------
    # Report result
    # --------------------------------------------------------------

    if not column_mismatches:

        print(
            f"{table_name}: PASS"
        )

    else:

        print(
            f"{table_name}: FAIL"
        )

        for mismatch in column_mismatches:

            mismatch_type = mismatch[0]

            if mismatch_type == "MISSING_IN_ORM":

                print(
                    "  Missing in ORM:"
                )

                for column in mismatch[1]:

                    print(
                        f"    - {column}"
                    )

            elif mismatch_type == "MISSING_IN_POSTGRESQL":

                print(
                    "  Missing in PostgreSQL:"
                )

                for column in mismatch[1]:

                    print(
                        f"    - {column}"
                    )

            elif mismatch_type == "COLUMN_DIFFERENCE":

                (
                    _,
                    column_name,
                    type_match,
                    nullable_match,
                    db_type,
                    orm_type,
                    db_timezone,
                    orm_timezone,
                    db_nullable,
                    orm_nullable,
                ) = mismatch

                print(
                    f"  Column: {column_name}"
                )

                if not type_match:

                    print(
                        "    TYPE:"
                    )

                    print(
                        f"      PostgreSQL: {db_type} "
                        f"(timezone={db_timezone})"
                    )

                    print(
                        f"      SQLAlchemy : {orm_type} "
                        f"(timezone={orm_timezone})"
                    )

                if not nullable_match:

                    print(
                        "    NULLABLE:"
                    )

                    print(
                        f"      PostgreSQL: {db_nullable}"
                    )

                    print(
                        f"      SQLAlchemy : {orm_nullable}"
                    )


# ======================================================================
# FOREIGN KEY AUDIT
# ======================================================================

print("\nFOREIGN KEY AUDIT")
print("-" * 70)


for table_name in common_tables:

    db_foreign_keys = inspector.get_foreign_keys(
        table_name
    )

    orm_table = Base.metadata.tables[table_name]

    # --------------------------------------------------------------
    # PostgreSQL foreign keys
    # --------------------------------------------------------------

    db_fk_set = set()

    for fk in db_foreign_keys:

        constrained_columns = fk[
            "constrained_columns"
        ]

        referred_columns = fk[
            "referred_columns"
        ]

        # Current schema uses single-column foreign keys.
        for local_column, remote_column in zip(
            constrained_columns,
            referred_columns,
        ):

            db_fk_set.add(
                (
                    local_column,
                    fk["referred_table"],
                    remote_column,
                    fk.get(
                        "options",
                        {},
                    ).get("ondelete"),
                    fk.get(
                        "options",
                        {},
                    ).get("onupdate"),
                )
            )

    # --------------------------------------------------------------
    # SQLAlchemy foreign keys
    # --------------------------------------------------------------

    orm_fk_set = set()

    for fk in orm_table.foreign_key_constraints:

        local_columns = list(
            fk.columns
        )

        elements = list(
            fk.elements
        )

        for local_column, element in zip(
            local_columns,
            elements,
        ):

            remote_column = element.column

            orm_fk_set.add(
                (
                    local_column.name,
                    remote_column.table.name,
                    remote_column.name,
                    fk.ondelete,
                    fk.onupdate,
                )
            )

    # --------------------------------------------------------------
    # Compare
    # --------------------------------------------------------------

    if db_fk_set == orm_fk_set:

        print(
            f"{table_name}: PASS"
        )

    else:

        print(
            f"{table_name}: FAIL"
        )

        db_only = (
            db_fk_set - orm_fk_set
        )

        orm_only = (
            orm_fk_set - db_fk_set
        )

        if db_only:

            print(
                "  Present in PostgreSQL "
                "but missing/different in ORM:"
            )

            for fk in sorted(db_only):
                print(
                    f"    {fk}"
                )

        if orm_only:

            print(
                "  Present in ORM "
                "but missing/different in PostgreSQL:"
            )

            for fk in sorted(orm_only):
                print(
                    f"    {fk}"
                )

# ======================================================================
# PRIMARY KEY AUDIT
# ======================================================================

print("\nPRIMARY KEY AUDIT")
print("-" * 70)


for table_name in common_tables:

    # --------------------------------------------------------------
    # PostgreSQL primary key
    # --------------------------------------------------------------

    db_pk = inspector.get_pk_constraint(table_name)

    db_pk_columns = tuple(
        db_pk.get("constrained_columns") or []
    )

    # --------------------------------------------------------------
    # SQLAlchemy primary key
    # --------------------------------------------------------------

    orm_table = Base.metadata.tables[table_name]

    orm_pk_columns = tuple(
        column.name
        for column in orm_table.primary_key.columns
    )

    # --------------------------------------------------------------
    # Compare
    # --------------------------------------------------------------

    if db_pk_columns == orm_pk_columns:

        print(
            f"{table_name}: PASS"
        )

    else:

        print(
            f"{table_name}: FAIL"
        )

        print(
            f"  PostgreSQL: {db_pk_columns}"
        )

        print(
            f"  SQLAlchemy : {orm_pk_columns}"
        )

# ======================================================================
# UNIQUE CONSTRAINT AUDIT
# ======================================================================

print("\nUNIQUE CONSTRAINT AUDIT")
print("-" * 70)


for table_name in common_tables:

    orm_table = Base.metadata.tables[table_name]

    # --------------------------------------------------------------
    # PostgreSQL unique constraints
    # --------------------------------------------------------------

    db_unique_constraints = inspector.get_unique_constraints(
        table_name
    )

    db_unique_set = {
        tuple(constraint["column_names"])
        for constraint in db_unique_constraints
    }

    # --------------------------------------------------------------
    # SQLAlchemy unique constraints
    # --------------------------------------------------------------

    orm_unique_set = {
        tuple(
            column.name
            for column in constraint.columns
        )
        for constraint in orm_table.constraints
        if constraint.__class__.__name__ == "UniqueConstraint"
    }

    # --------------------------------------------------------------
    # Compare constrained columns
    # --------------------------------------------------------------

    if db_unique_set == orm_unique_set:

        print(
            f"{table_name}: PASS"
        )

    else:

        print(
            f"{table_name}: FAIL"
        )

        db_only = db_unique_set - orm_unique_set
        orm_only = orm_unique_set - db_unique_set

        if db_only:

            print(
                "  Unique constraints present in PostgreSQL "
                "but missing in ORM:"
            )

            for columns in sorted(db_only):
                print(
                    f"    - {columns}"
                )

        if orm_only:

            print(
                "  Unique constraints present in ORM "
                "but missing in PostgreSQL:"
            )

            for columns in sorted(orm_only):
                print(
                    f"    - {columns}"
                )

# ======================================================================
# CHECK CONSTRAINT AUDIT
# ======================================================================

print("\nCHECK CONSTRAINT AUDIT")
print("-" * 70)


for table_name in common_tables:

    orm_table = Base.metadata.tables[table_name]

    # --------------------------------------------------------------
    # PostgreSQL CHECK constraints
    # --------------------------------------------------------------

    db_check_constraints = inspector.get_check_constraints(
        table_name
    )

    db_check_set = {
        constraint["name"]
        for constraint in db_check_constraints
    }

    # --------------------------------------------------------------
    # SQLAlchemy CHECK constraints
    # --------------------------------------------------------------

    orm_check_set = {
        constraint.name
        for constraint in orm_table.constraints
        if constraint.__class__.__name__ == "CheckConstraint"
        and constraint.name is not None
    }

    # --------------------------------------------------------------
    # Compare
    # --------------------------------------------------------------

    if db_check_set == orm_check_set:

        print(
            f"{table_name}: PASS"
        )

    else:

        print(
            f"{table_name}: FAIL"
        )

        db_only = db_check_set - orm_check_set
        orm_only = orm_check_set - db_check_set

        if db_only:

            print(
                "  Present in PostgreSQL "
                "but missing in ORM:"
            )

            for constraint in sorted(db_only):
                print(
                    f"    - {constraint}"
                )

        if orm_only:

            print(
                "  Present in ORM "
                "but missing in PostgreSQL:"
            )

            for constraint in sorted(orm_only):
                print(
                    f"    - {constraint}"
                )

# ======================================================================
# INDEX AUDIT
# ======================================================================

print("\nINDEX AUDIT")
print("-" * 70)


def normalize_index_predicate(predicate):
    """
    Normalize PostgreSQL/SQLAlchemy formatting differences
    in partial-index predicates.
    """

    if predicate is None:
        return None

    predicate = str(predicate).strip()

    # PostgreSQL inspector may return:
    # (is_current = true)
    #
    # SQLAlchemy may return:
    # is_current = true

    while (
        predicate.startswith("(")
        and predicate.endswith(")")
    ):
        predicate = predicate[1:-1].strip()

    # Normalize whitespace.
    predicate = " ".join(
        predicate.split()
    )

    return predicate


for table_name in common_tables:

    orm_table = Base.metadata.tables[table_name]

    # --------------------------------------------------------------
    # PostgreSQL unique constraints
    #
    # Their backing indexes are NOT treated as explicit indexes
    # because they are already audited separately.
    # --------------------------------------------------------------

    db_unique_constraints = inspector.get_unique_constraints(
        table_name
    )

    unique_constraint_names = {
        constraint["name"]
        for constraint in db_unique_constraints
        if constraint.get("name")
    }

    # --------------------------------------------------------------
    # PostgreSQL indexes
    # --------------------------------------------------------------

    db_indexes = inspector.get_indexes(
        table_name
    )

    db_index_set = set()

    for index in db_indexes:

        index_name = index["name"]

        # Skip indexes automatically created for UNIQUE constraints.
        if index_name in unique_constraint_names:
            continue

        predicate = normalize_index_predicate(
            index.get(
                "dialect_options",
                {},
            ).get(
                "postgresql_where"
            )
        )

        db_index_set.add(
            (
                index_name,
                tuple(
                    index["column_names"]
                ),
                index.get(
                    "unique",
                    False,
                ),
                predicate,
            )
        )

    # --------------------------------------------------------------
    # SQLAlchemy indexes
    # --------------------------------------------------------------

    orm_index_set = set()

    for index in orm_table.indexes:

        predicate = index.dialect_options.get(
            "postgresql",
            {},
        ).get(
            "where"
        )

        predicate = normalize_index_predicate(
            predicate
        )

        orm_index_set.add(
            (
                index.name,
                tuple(
                    column.name
                    for column in index.columns
                ),
                index.unique,
                predicate,
            )
        )

    # --------------------------------------------------------------
    # Compare
    # --------------------------------------------------------------

    if db_index_set == orm_index_set:

        print(
            f"{table_name}: PASS"
        )

    else:

        print(
            f"{table_name}: FAIL"
        )

        db_only = (
            db_index_set
            - orm_index_set
        )

        orm_only = (
            orm_index_set
            - db_index_set
        )

        if db_only:

            print(
                "  Present in PostgreSQL "
                "but missing/different in ORM:"
            )

            for index in sorted(
                db_only,
                key=str,
            ):
                print(
                    f"    {index}"
                )

        if orm_only:

            print(
                "  Present in ORM "
                "but missing/different in PostgreSQL:"
            )

            for index in sorted(
                orm_only,
                key=str,
            ):
                print(
                    f"    {index}"
                )

# ======================================================================
# ORM RELATIONSHIP AUDIT
# ======================================================================

print("\nORM RELATIONSHIP AUDIT")
print("-" * 70)


expected_relationships = {
    "User": {
        "projects": "Project",
        "experiences": "Experience",
        "education": "Education",
        "certifications": "Certification",
        "posts": "Post",
        "resumes": "Resume",
    },

    "Project": {
        "owner": "User",
        "skills": "Skill",
    },

    "SkillCategory": {
        "skills": "Skill",
    },

    "Skill": {
        "skill_category": "SkillCategory",
        "projects": "Project",
        "experiences": "Experience",
    },

    "Experience": {
        "owner": "User",
        "skills": "Skill",
    },

    "Education": {
        "owner": "User",
    },

    "Certification": {
        "owner": "User",
    },

    "Post": {
        "owner": "User",
    },

    "Resume": {
        "owner": "User",
    },

    "ProjectSkill": {},

    "ExperienceSkill": {},

    "ContactMessage": {},

    "VisitorLog": {},

    "SyncLog": {},
}


for model_name, expected in expected_relationships.items():

    # --------------------------------------------------------------
    # Get ORM model
    # --------------------------------------------------------------

    model = globals()[model_name]

    actual_relationships = {
        relationship.key: relationship.mapper.class_.__name__
        for relationship in model.__mapper__.relationships
    }

    # --------------------------------------------------------------
    # Compare relationship names and targets
    # --------------------------------------------------------------

    expected_set = set(
        expected.items()
    )

    actual_set = set(
        actual_relationships.items()
    )

    if expected_set == actual_set:

        print(
            f"{model_name}: PASS"
        )

    else:

        print(
            f"{model_name}: FAIL"
        )

        missing = expected_set - actual_set
        unexpected = actual_set - expected_set

        if missing:

            print(
                "  Missing relationships:"
            )

            for relationship in sorted(
                missing
            ):

                print(
                    f"    - {relationship[0]} "
                    f"→ {relationship[1]}"
                )

        if unexpected:

            print(
                "  Unexpected relationships:"
            )

            for relationship in sorted(
                unexpected
            ):

                print(
                    f"    - {relationship[0]} "
                    f"→ {relationship[1]}"
                )
print("\n" + "=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)