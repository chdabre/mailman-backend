from celery import shared_task
from postcard_creator.postcard_creator import PostcardCreator

from jobs.models import Address


@shared_task
def import_user_address(credentials):
    try:
        Address.objects.get(user=credentials.user, is_primary=True)
    except Address.DoesNotExist:
        token = credentials.get_token()
        client = PostcardCreator(token)

        user_info = client.get_user_info()
        address = Address.objects.create(
            user=credentials.user,
            is_primary=True,
            firstname=user_info['firstName'],
            lastname=user_info['name'],
            street=user_info['street'],
            zipcode=user_info['zip'],
            city=user_info['city'],
        )
        address.save()