from apps.event.mixins.tests.event import EventTestMixin
from apps.event.models import Event, UserEventRelation
from apps.event.sub.subserializers import EventListSerializer
from apps.utils import ClientTestMixin, UserCreationTestMixin


class RelationTest(ClientTestMixin, EventTestMixin, UserCreationTestMixin):
    @staticmethod
    def get_ignore_and_qs():
        relations = UserEventRelation.objects.all()
        ignore_amount = set(relations.values_list("ignore", flat=True).distinct())
        
        return relations, ignore_amount
    
    def test_relation(self):
        with self.Login_user_as_context() as user:
            for _ in range(10):
                self.Create_event()
            
            self.assertGreater(UserEventRelation.objects.all().count(), 0)
            
            event = Event.objects.first()
            
            response = self.client.patch(
                f"/api/user-relation/event/{event.scooso_id}/",
                {
                    "ignore": True
                },
                content_type="application/json"
            )
            
            self.assertStatusOk(response.status_code)
            
            # Get events
            response = self.client.get(
                "/api/event/",
                {
                    "ignore": True
                },
                content_type="application/json"
            )
            
            self.assertStatusOk(response.status_code)
            self.assertCountEqual(
                response.data["results"],
                EventListSerializer(Event.objects.filter(
                    usereventrelation__user=user,
                    usereventrelation__ignore=True
                ), many=True).data
            )
        
        with self.Login_user_as_context() as user:
            
            # Get event
            response = self.client.get(
                "/api/event/",
                {
                    "ignore": False
                },
                content_type="application/json"
            )
            events = Event.objects.filter(
                usereventrelation__user=user,
                usereventrelation__ignore=False
            )
            
            self.assertStatusOk(response.status_code)
            self.assertCountEqual(
                response.data["results"], EventListSerializer(events, many=True).data
            )
    
    def test_user_created_after_object_created(self):
        with self.Login_user_as_context() as _:
            self.Create_event()
            before_create_count = UserEventRelation.objects.all().count()
            self.assertEqual(before_create_count, 1)
            
            self.Create_event()
            after_create_count = UserEventRelation.objects.all().count()
            self.assertEqual(after_create_count, 2)
