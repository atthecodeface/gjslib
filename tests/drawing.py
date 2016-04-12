#!/usr/bin/env python
#a Imports
import gjslib.graphics.draw_buffer
import unittest

class DrawBufferTests(unittest.TestCase):
    def check_buffer(self,d,value):
        dl = d.__repr__().split("\n")
        for i in range(len(dl)):
            self.assertEqual(value[i],dl[i], 'Bad draw buffer data')
        pass
    def test_tiny_dot(self):
        d = gjslib.graphics.draw_buffer.draw_buffer(mode="1",size=(4,4))
        d.set_pixel(1,1)
        return self.check_buffer(d,['    ', ' *  ', '    ', '    ', ''])
    def test_tiny_horiz(self):
        d = gjslib.graphics.draw_buffer.draw_buffer(mode="1",size=(4,4))
        d.draw_line( (0,0,4,0), value=64 )
        d.draw_line( (0,1,4,1), value=255 )
        d.draw_line( (0,2,4,2), value=128 )
        d.draw_line( (0,3,4,3), value=192 )
        return self.check_buffer(d,['....', '****', '....', '****', ''])
    def test_tiny_vert(self):
        d = gjslib.graphics.draw_buffer.draw_buffer(mode="1",size=(4,4))
        d.draw_line( (0,0,0,4), value=64 )
        d.draw_line( (1,0,1,4), value=255 )
        d.draw_line( (2,0,2,4), value=128 )
        d.draw_line( (3,0,3,4), value=192 )
        return self.check_buffer(d,['.*.*', '.*.*', '.*.*', '.*.*', ''])
    def test_tiny_diag_dr(self):
        d = gjslib.graphics.draw_buffer.draw_buffer(mode="1",size=(4,4))
        d.draw_line( (0,0,4,4), value=64 )
        d.draw_line( (1,0,5,4), value=255 )
        d.draw_line( (2,0,6,4), value=128 )
        d.draw_line( (3,0,7,4), value=192 )
        return self.check_buffer(d,['.*.*', '.*.*', ' .*.', '  .*', ''])
    def test_tiny_diag_dl(self):
        d = gjslib.graphics.draw_buffer.draw_buffer(mode="1",size=(4,4))
        d.draw_line( (4,0,0,4), value=64 )
        d.draw_line( (3,0,0,3), value=255 )
        d.draw_line( (2,0,0,2), value=128 )
        d.draw_line( (1,0,0,1), value=192 )
        return self.check_buffer(d,[' *.*', '**.*', '..*.', '**. ', ''])
    def test_tiny_diag_fill_center(self):
        d = gjslib.graphics.draw_buffer.draw_buffer(mode="1",size=(4,4))
        d.fill_paths( [((0.9,0.9), (0.9,2.1), (2.1,2.1), (2.1,0.9),),
                   ],value=255 )
        return self.check_buffer(d,['    ', '**  ', '**  ', '    ', ''])
    def test_tiny_diag_fill_rings(self):
        d = gjslib.graphics.draw_buffer.draw_buffer(mode="1",size=(8,8))
        p = []
        for i in [1,2,3,4]:
            p.append( ( (i-0.1, i-0.1), (i-0.1, 8.1-i), (8.1-i, 8.1-i), (8.1-i, i-0.1)) )
            pass
        d.fill_paths( p, value=64 )
        return self.check_buffer(d,['        ', '....... ', '.     . ', '. ... . ', '. . . . ', '. ... . ', '.     . ', '....... ', ''])

suite = unittest.TestLoader().loadTestsFromTestCase(DrawBufferTests)

if __name__ == '__main__':
    unittest.main()
