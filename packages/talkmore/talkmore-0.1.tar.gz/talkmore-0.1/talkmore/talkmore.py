import requests
import json
import re

class UserNotLoggedIn(Exception):
    pass

class ContactDeletionException(Exception):
    pass

class Talkmore:

    def __init__(self, username, password):
        self.session = requests.session()
        self.login_data = {'item': '', 'scController': 'Login', 'scAction': 'Login', 'redirectUrl': ''}
        self.login_data.update([('phoneNumber', username), ('password', password)])
        self.username = username

    def login(self):
        self.session.post('https://talkmore.no/login', data=self.login_data)
        return self.is_logged_in()

    def is_logged_in(self):
        return ('accesstoken-prod' in self.session.cookies.keys())

    def send_sms(self, recipients, message):
        if not self.is_logged_in():
            raise UserNotLoggedIn('User not logged in. Call .login() first')
        if isinstance(recipients, str):
            recipients = [recipients]
        if len(message) >= 1600:
            first_message = message[:1599]
            self.send_sms(recipients, first_message)
            next_message = message[1599:]
            self.send_sms(recipients, next_message)
        data = {"Recipients": recipients, "Message": message}
        r = self.session.post('https://talkmore.no/tmapi/sms/send', data=data)
        return (r.status_code == 200)

    def send_sms_to_all_contacts(self, message, send_to_self=False):
        contacts = self.get_contacts()
        clean_contacts = list()
        for contact in contacts:
            clean_contacts.append(contact.get('phone'))
        if send_to_self is False:
            try:
                clean_contacts.remove(self.username)
            except:
                pass
        return self.send_sms(clean_contacts, message)

    def add_contact(self, first_name, last_name, phone_number):
        data = {
            'scController': 'SendSms',
            'scAction': 'AddSmsContact',
            'firstName': first_name,
            'lastName': last_name,
            'phoneNumber': phone_number
        }
        r = self.session.post('https://talkmore.no/minesider/sms', data=data)
        return r

    def get_contacts(self):
        r = self.add_contact('Captain', 'Placeholder', self.username)
        rendered_contact_list = r.json().get('RenderedContactList')
        c_id = self.find_contact_id_by_name_and_phone_number('Captain Placeholder', self.username, rendered_contact_list)
        self.delete_contact(c_id)
        return r.json().get('ContactItems')

    def find_contact_id_by_name_and_phone_number(self, name, phone_number, contact_list):
        c_id = re.search(f'label for="(.*)">{name} - {phone_number}</label>', contact_list).group(1)
        return c_id

    def find_contact_id_by_phone_number(self, phone_number, contact_list=None):
        if contact_list is None:
            contact_list = self.get_contacts()
        contact_ids = list()
        for div in contact_list.split('</div>'):
            if phone_number in div:
                contact_id = re.search('id="(.*)"', div).group(1)
                contact_ids.append(contact_id)
        return contact_ids

    def delete_contact(self, contact_id):
        if isinstance(contact_id, list()):
            contact_id = contact_id[0]
        data = {
            'scController': 'SendSms',
            'scAction': 'DeleteSmsContact',
            'contactId': contact_id
        }
        r = self.session.post('https://talkmore.no/minesider/sms', data=data)
        return r.json().get('Success')

    def delete_contacts(self, contacts):
        for contact in contacts:
            self.delete_contact(contact)

    def delete_duplicate_contacts(self, contact_list, phone_number):
        for div in contact_list.split('</div>'):
            if phone_number in div:
                contact_id = re.search('id="(.*)"', div).group(1)
                if not self.delete_contact(contact_id):
                    raise ContactDeletionException(f'Failed to delete contact {contact_id}')
        return True

if __name__ == '__main__':
    talkmore = Talkmore('99999999', 'password')
    talkmore.login()
    talkmore.send_sms('98989898', 'Message goes here')

