import sqlalchemy.dialects.postgresql
import uuid
import sqlalchemy.types as types

try:
    # Check if the psycopg2 module exists
    import psycopg2.extras

    # Required for PostgreSQL to accept UUID type.
    psycopg2.extras.register_uuid()
except ImportError:
    pass


class ChoiceType(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class UUID(types.TypeDecorator):
    """ Converts UUID to string before storing to database.
        Converts string to UUID when retrieving from database. """

    impl = types.TypeEngine

    def load_dialect_impl(self, dialect):
        """ When using Postgres database, use the Postgres UUID column type.
            Otherwise, use String column type. """
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(sqlalchemy.dialects.postgresql.UUID)

        return dialect.type_descriptor(types.String)

    def process_bind_param(self, value, dialect):
        """ When using Postgres database, check that is a valid uuid and
            store as UUID object.
            Otherwise, convert to string before storing to database. """

        if value is None:
            return value

        if not isinstance(value, UUID):
            # Try to convert to UUID to check validity
            value = uuid.UUID(value)

        if dialect.name == 'postgres':
            return value

        return str(value).replace('-', '')

    def process_result_value(self, value, dialect):
        """ When using Postgres database, convert to string before returning value.
            Otherwise, provide as is. """
        if dialect.name == 'postgresql':
            return str(value).replace('-', '')

        if value is None:
            return value

        return value