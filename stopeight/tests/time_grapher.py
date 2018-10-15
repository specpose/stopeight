from stopeight.util.editor.modules.file_wave import _convert
import wave
from stopeight.util.editor.data import WaveData,ScribbleData,ScribblePoint
from stopeight.util.editor.modules.grapher import _append
from stopeight.grapher import create_vector_graph
import numpy as np

if __name__ == '__main__':
    filename = "afterstanley3-bass.wav"
    spf = wave.open(filename,'r')
    result = _convert(spf)
    spf.close()
    data = result.view(WaveData)
    result = create_vector_graph(data,1,1.0,True)
    assert type(result) is np.ndarray, "Cast Error: %r" % type(result)
    result = _append(result)
    print("Return Length "+str(len(result)))
    #Hack copy 2
    #extractor = lambda c:c['coords']
    #array = np.fromfunction(extractor(result),(2,2),dtype=np.float64)
    #array=ScribbleData(size=len(result))
    #for i,v in enumerate(result):
    #    array[i] = [v['coords'][0],v['coords'][1]]
    array = result.view(ScribbleData)
    print(array)
    print(type(array))
    print(len(array))