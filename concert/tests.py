from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Concert, ConcertAttending

class BandWebsiteTests(TestCase):
    def test_public_pages_and_lyrics(self):
        self.assertContains(self.client.get(reverse('index')), 'Djirection')
        self.assertContains(self.client.get(reverse('songs')), 'Lyrics')
        self.assertContains(self.client.get(reverse('photos')), 'Washington')

    def test_signup_login_logout_and_concert_attendance(self):
        concert = Concert.objects.create(concert_name='Coachella 2023', duration=72, city='Indio, California')
        self.assertRedirects(self.client.get(reverse('concerts')), reverse('login'))
        self.assertRedirects(self.client.post(reverse('signup'), {'username':'testfan','password':'lab-password'}), reverse('index'))
        self.assertNotEqual(User.objects.get(username='testfan').password, 'lab-password')
        self.assertContains(self.client.get(reverse('concerts')), 'Coachella 2023')
        self.assertRedirects(self.client.post(reverse('concert_attendee'), {'concert_id':concert.id,'attendee_choice':'Attending'}), reverse('concerts'))
        self.assertEqual(ConcertAttending.objects.get().attending, 'Attending')
        self.client.get(reverse('logout'))
        self.assertRedirects(self.client.get(reverse('concerts')), reverse('login'))
        self.assertRedirects(self.client.post(reverse('login'), {'username':'testfan','password':'lab-password'}), reverse('index'))

    def test_duplicate_signup_does_not_replace_password(self):
        User.objects.create_user('existing', password='original-password')
        response = self.client.post(reverse('signup'), {'username':'existing','password':'different-password'})
        self.assertContains(response, 'user already exist')
        self.assertTrue(User.objects.get(username='existing').check_password('original-password'))
