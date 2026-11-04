"""Run with: python -m unittest discover -s tests -p test_redis_config.py."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class RedisConfigurationTests(unittest.TestCase):
    def read_configuration(self, environment_url=None, dotenv_url=None):
        # Isolate .env discovery from developer credentials and other API imports.
        source = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ("api/core/config.py", "api/celery_tasks/app.py"):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / relative, target)
            if dotenv_url is not None:
                (root / ".env").write_text(f"REDIS_URL={dotenv_url}\n")
            environment = os.environ.copy()
            environment.pop("REDIS_URL", None)
            environment.pop("PYTHON_DOTENV_DISABLED", None)
            environment["PYTHONPATH"] = str(root)
            if environment_url is not None:
                environment["REDIS_URL"] = environment_url
            result = subprocess.run(
                [sys.executable, "-c", """
import json
from api.celery_tasks.app import celery_app, masked_redis_url
from api.core.config import REDIS_URL
print(json.dumps([REDIS_URL, celery_app.conf.broker_url,
                  celery_app.conf.result_backend, masked_redis_url]))
"""],
                cwd=root, env=environment, check=True, text=True,
                capture_output=True,
            )
            return json.loads(result.stdout)

    def test_worker_loads_dotenv_and_masks_password(self):
        url = "redis://default:test-password@redis.example.com:13424/0"
        values = self.read_configuration(dotenv_url=url)
        self.assertEqual(values[:3], [url] * 3)
        self.assertEqual(values[3], "redis://default:******@redis.example.com:13424/0")

    def test_deployment_environment_takes_precedence(self):
        url = "redis://default:deployment-password@new.example.com:13424/0"
        values = self.read_configuration(
            environment_url=url, dotenv_url="redis://old.example.com:6379/0"
        )
        self.assertEqual(values[:3], [url] * 3)

    def test_local_default_is_shared(self):
        for value in (None, ""):
            with self.subTest(environment_url=value):
                values = self.read_configuration(environment_url=value)
                self.assertEqual(values[:3], ["redis://localhost:6379/0"] * 3)
