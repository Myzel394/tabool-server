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
            for _ in range(20):
                self.Create_event()
            
            self.assertGreater(UserEventRelation.objects.all().count(), 0)
            
            event = Event.objects.all().first()
            relations, ignore_amount = self.get_ignore_and_qs()
            
            response = self.client.patch(
                f"/api/user-relation/event/{event.id}/",
                {
                    "ignore": True
                },
                content_type="application/json"
            )
            
            self.assertStatusOk(response.status_code)
            relations, ignore_amount = self.get_ignore_and_qs()
            
            # Get event
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
                EventListSerializer(Event.objects.all().filter(
                    usereventrelation__user=user,
                    usereventrelation__ignore=True
                ), many=True).data
            )
        
        relations, ignore_amount = self.get_ignore_and_qs()
        with self.Login_user_as_context() as user:
            
            # Get event
            response = self.client.get(
                "/api/event/",
                {
                    "ignore": True
                },
                content_type="application/json"
            )
            relations, ignore_amount = self.get_ignore_and_qs()
            
            self.assertStatusOk(response.status_code)
            self.assertCountEqual(
                response.data["results"],
                EventListSerializer(Event.objects.all().filter(
                    usereventrelation__user=user,
                    usereventrelation__ignore=False
                ), many=True).data
            )
