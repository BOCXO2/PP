import unittest
import json
import yaml
import os
from app import app, process_text, process_json, process_yaml, process_xml

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def tearDown(self):
        for file in os.listdir(self.upload_folder):
            os.remove(os.path.join(self.upload_folder, file))

    def test_process_text(self):
        input_text = "(5 + 3) - 2\n12 - 4\n7 * 2\n15 / 3"
        expected_output = "6\n8\n14\n5.0"
        self.assertEqual(process_text(input_text), expected_output)

    def test_process_json(self):
        input_json = json.dumps({
            "expressions": ["5 + 3", "(10 - 2) * 3", "14 / 2 + 6"],
            "details": {"nested": "(8 + 2) * (3 - 1)"}
        })
        expected_output = json.dumps({
            "expressions": ["8", "24", "13.0"],
            "details": {"nested": "20"}
        }, indent=4)
        self.assertEqual(process_json(input_json), expected_output)

    def test_process_yaml(self):
        input_yaml = """
        expressions:
          - "5 + 3"
          - "(10 - 2) * 3"
          - "14 / 2 + 6"
        details:
          nested: "(8 + 2) * (3 - 1)"
        """
        expected_output = """
        expressions:
        - "8"
        - "24"
        - "13.0"
        details:
          nested: "20"
        """.strip()
        self.assertEqual(process_yaml(input_yaml).strip(), expected_output)

    def test_process_yaml(self):
        input_yaml = """
        expressions:
        - "5 + 3"
        - "(10 - 2) * 3"
        - "14 / 2 + 6"
        details:
        nested: "(8 + 2) * (3 - 1)"
        """
        expected_output = yaml.safe_load("""
        expressions:
        - "8"
        - "24"
        - "13.0"
        details:
        nested: "20"
        """)
        actual_output = yaml.safe_load(process_yaml(input_yaml))
        self.assertEqual(actual_output, expected_output)


    def test_upload_file(self):
        test_content = "(5 + 3) - 2\n12 - 4\n7 * 2\n15 / 3"
        with open(os.path.join(self.upload_folder, "test.txt"), "w", encoding="utf-8") as test_file:
            test_file.write(test_content)

        with open(os.path.join(self.upload_folder, "test.txt"), "rb") as test_file:
            data = {"file": (test_file, "test.txt")}
            response = self.client.post('/upload', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn("output_file", json_data)

        output_file_path = json_data["output_file"]
        with open(output_file_path, 'r', encoding='utf-8') as f:
            processed_content = f.read()
        self.assertEqual(processed_content, "6\n8\n14\n5.0")


if __name__ == '__main__':
    unittest.main()
