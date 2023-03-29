from .queries import retrieve_template_query


async def get_template_for_payment(session, template_id):
    query = retrieve_template_query(template_id)
    data = await session.execute(query)
    return data.first()
