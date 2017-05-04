import json
import unittest

import scomodels as models
import scodata.mongo as mongo

MODELS_FILE = './data/models.json'

class TestModelRegistryMethods(unittest.TestCase):

    def setUp(self):
        """Connect to MongoDB and clear an existing model collection.
        Create model regisrty manager"""
        # Read model definitions
        with open(MODELS_FILE, 'r') as f:
            self.models = json.load(f)
        m = mongo.MongoDBFactory(db_name='scotest')
        db = m.get_database()
        db.models.drop()
        self.registry = models.DefaultModelRegistry(db.models)

    def test_delete_models(self):
        """Test creation of model objects."""
        # Create model from Json document
        count = 0
        models = []
        for i in range(len(self.models)):
            model = self.registry.from_json(self.models[i])
            self.registry.register_model(
                model.identifier,
                model.properties,
                model.parameters
            )
            count += 1
            models.append(model.identifier)
        # Make sure that we can get all the models
        for id in models:
            self.assertIsNotNone(self.registry.get_model(id))
        # Delete one model after the other
        while count > 0:
            self.registry.delete_model(models[count - 1])
            count -= 1
            listing = self.registry.list_models()
            self.assertEqual(len(listing.items), count)
            self.assertEqual(listing.total_count, count)
            self.assertIsNone(self.registry.get_model(models[count]))

    def test_list_models(self):
        """Test creation of model objects."""
        # Create model from Json document
        count = 0
        for i in range(len(self.models)):
            model = self.registry.from_json(self.models[i])
            self.registry.register_model(
                model.identifier,
                model.properties,
                model.parameters
            )
            count += 1
        listing = self.registry.list_models()
        self.assertEqual(len(listing.items), count)
        self.assertEqual(listing.total_count, count)

    def test_register_model(self):
        """Test creation of model objects."""
        # Create model from Json document
        for i in range(len(self.models)):
            model = self.registry.from_json(self.models[i])
            # Insert model
            m = self.registry.register_model(
                model.identifier,
                model.properties,
                model.parameters
            )
            # Assert that identifier and name
            self.assertEqual(m.identifier, model.identifier)
            self.assertEqual(m.name, model.name)
            # Get model
            m = self.registry.get_model(model.identifier)
            # Assert that identifier and name are the same
            self.assertEqual(m.identifier, model.identifier)
            self.assertEqual(m.name, model.name)


if __name__ == '__main__':
    unittest.main()
