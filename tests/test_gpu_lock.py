import subprocess,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
from gpu_lock import acquire
class LockTest(unittest.TestCase):
 def test_second_process_is_rejected_then_can_acquire_after_release(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'gpu.lock'
   handle=acquire(path)
   code="import sys;sys.path.insert(0,sys.argv[1]);from gpu_lock import acquire;from pathlib import Path;acquire(Path(sys.argv[2]))"
   command=[sys.executable,'-c',code,str(Path(__file__).resolve().parents[1]/'pipeline'),str(path)]
   r=subprocess.run(command,capture_output=True,text=True)
   self.assertNotEqual(r.returncode,0)
   self.assertIn('Another factory GPU job',r.stderr)
   handle.close()
   self.assertEqual(subprocess.run(command,capture_output=True).returncode,0)
if __name__=='__main__': unittest.main()
