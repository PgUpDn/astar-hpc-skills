"""Offline behavioral checks; no cluster access, real credentials or jobs required."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gateway', ROOT / 'skills/acrc-hpc/scripts/gateway_check.py')
gateway = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gateway)


class Reply(io.BytesIO):
    def __init__(self, value):
        super().__init__(json.dumps(value).encode())


class GatewayTests(unittest.TestCase):
    def run_check(self, replies, model=None, base='https://gateway.example.invalid'):
        opener = mock.Mock()
        opener.open.side_effect = replies
        output = io.StringIO()
        with mock.patch.dict(os.environ, {'ACRC_GATEWAY_BASE_URL': base, 'ACRC_GATEWAY_API_KEY': 'test-only-secret'}), \
                mock.patch.object(gateway.urllib.request, 'build_opener', return_value=opener), \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = gateway.check(model)
        self.assertNotIn('test-only-secret', output.getvalue())
        return code, output.getvalue(), opener

    def test_list_does_not_infer(self):
        code, output, opener = self.run_check([Reply({'data': [{'id': 'example-model'}]})])
        self.assertEqual(code, 0)
        self.assertEqual(opener.open.call_count, 1)
        self.assertEqual(json.loads(output)['models'], ['example-model'])

    def test_completion_and_v1_normalization(self):
        code, _, opener = self.run_check([
            Reply({'data': [{'id': 'example-model'}]}),
            Reply({'choices': [{'message': {'content': 'OK'}}]})],
            'example-model', 'https://gateway.example.invalid/v1/')
        self.assertEqual(code, 0)
        self.assertEqual(opener.open.call_args[0][0].full_url,
                         'https://gateway.example.invalid/v1/chat/completions')

    def test_unknown_model_sends_no_completion(self):
        code, _, opener = self.run_check([Reply({'data': []})], 'missing')
        self.assertEqual(code, 2)
        self.assertEqual(opener.open.call_count, 1)

    def test_no_content_is_failure(self):
        code, _, _ = self.run_check([Reply({'data': [{'id': 'm'}]}),
                                    Reply({'choices': [{'message': {'content': ''}}]})], 'm')
        self.assertEqual(code, 1)

    def test_http_failure_suppresses_sensitive_body(self):
        failure = urllib.error.HTTPError('https://example.invalid', 401,
                                         'test-only-secret', {}, Reply({'error': 'test-only-secret'}))
        code, output, _ = self.run_check([failure])
        self.assertEqual(code, 1)
        self.assertIn('401', output)

    def test_bad_response_is_failure(self):
        code, _, _ = self.run_check([Reply([])])
        self.assertEqual(code, 1)

    def test_insecure_url_is_rejected(self):
        code, _, opener = self.run_check([], base='http://gateway.example.invalid')
        self.assertEqual(code, 2)
        opener.open.assert_not_called()

    def test_redirect_is_not_followed(self):
        self.assertIsNone(gateway.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://elsewhere.invalid'))


class TemplateTests(unittest.TestCase):
    def test_shell_syntax(self):
        for path in (ROOT / 'skills').rglob('*'):
            if path.suffix in {'.sh', '.pbs', '.sbatch'}:
                subprocess.run(['bash', '-n', str(path)], check=True, capture_output=True)

    def test_scan_handles_names_and_does_not_follow_symlinks(self):
        source = (ROOT / 'skills/nscc-hpc/assets/scan.pbs').read_text()
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            tree = work / 'tree'
            tree.mkdir()
            (tree / 'a space').write_bytes(b'abc')
            (tree / 'line\nbreak').write_bytes(b'12345')
            (tree / 'link').symlink_to(work)
            script = work / 'scan.pbs'
            script.write_text(source.replace('REPLACE_ABSOLUTE_DIRECTORY', str(tree)))
            env = dict(os.environ, PBS_O_WORKDIR=str(work), PBS_JOBID='offline')
            result = subprocess.run(['bash', str(script)], env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            rows = {row['entry']: row for row in json.loads((work / 'inventory-offline.json').read_text())}
            self.assertEqual(rows['a space']['bytes'], 3)
            self.assertEqual(rows['line\nbreak']['bytes'], 5)
            self.assertEqual(rows['link']['files'], 0)
            self.assertEqual(rows['link']['symlinks'], 1)
            second = subprocess.run(['bash', str(script)], env=env, capture_output=True)
            self.assertNotEqual(second.returncode, 0, 'An existing inventory must not be overwritten')

    def test_missing_scheduler_does_not_report_success(self):
        with tempfile.TemporaryDirectory() as temp:
            env = dict(os.environ, ACRC_PROJECT_DIR=temp, PATH='/nonexistent')
            result = subprocess.run(['/bin/bash', str(ROOT / 'skills/acrc-hpc/scripts/acrc_status.sh')],
                                    env=env, capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
