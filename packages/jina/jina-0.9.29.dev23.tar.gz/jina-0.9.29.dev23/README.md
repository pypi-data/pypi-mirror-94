<p align="center">
<img src="https://github.com/jina-ai/jina/blob/master/.github/logo-only.gif?raw=true" alt="Jina banner" width="200px">
</p>
<p align="center">
An easier way to build neural search in the cloud
</p>
<p align=center>
<a href="#license"><img src="https://github.com/jina-ai/jina/blob/master/.github/badges/license-badge.svg?raw=true" alt="Jina" title="Jina is licensed under Apache-2.0"></a>
<a href="https://pypi.org/project/jina/"><img src="https://github.com/jina-ai/jina/blob/master/.github/badges/python-badge.svg?raw=true" alt="Python 3.7 3.8 3.9" title="Jina supports Python 3.7 and above"></a>
<a href="https://pypi.org/project/jina/"><img src="https://img.shields.io/pypi/v/jina?color=%23099cec&amp;label=PyPI&amp;logo=pypi&amp;logoColor=white" alt="PyPI"></a>
<a href="https://hub.docker.com/r/jinaai/jina/tags"><img src="https://img.shields.io/docker/v/jinaai/jina?color=%23099cec&amp;label=Docker&amp;logo=docker&amp;logoColor=white&amp;sort=semver" alt="Docker Image Version (latest semver)"></a>
<a href="https://github.com/jina-ai/jina/actions?query=workflow%3ACI"><img src="https://github.com/jina-ai/jina/workflows/CI/badge.svg" alt="CI"></a>
<a href="https://github.com/jina-ai/jina/actions?query=workflow%3ACD"><img src="https://github.com/jina-ai/jina/workflows/CD/badge.svg?branch=master" alt="CD"></a>
<a href="https://codecov.io/gh/jina-ai/jina"><img src="https://codecov.io/gh/jina-ai/jina/branch/master/graph/badge.svg" alt="codecov"></a>
</p>


Jina is a deep learning-powered search framework for building <strong>cross-/multi-modal search systems</strong> (e.g. text, images, video, audio) in the cloud. 

⏱️ **Time Saver** - *The* design pattern of neural search systems, from zero to a production-ready system in minutes.

🌌 **Universal Search** - Large-scale indexing and querying of unstructured data: video, image, long/short text, music, source code, etc.

🧠 **First-Class AI Models** - First-class support for [state-of-the-art AI models](https://docs.jina.ai/chapters/all_exec.html).

☁️  **Cloud Ready** - Decentralized architecture with cloud-native features out-of-the-box: containerization, microservice, scaling, sharding, async IO, REST, gRPC, WebSocket.

🧩 **Plug & Play** - Easily usable and extendable with a Pythonic interface.

❤️  **Made with Love** - Lean dependencies (only 6!) & tip-top, never compromises on quality, maintained by a [passionate full-time, venture-backed team](https://jina.ai).

---

<p align="center">
<a href="http://docs.jina.ai">Docs</a> • <a href="#jina-hello-world-">Hello World</a> • <a href="#get-started">Quick Start</a> • <a href="#learn">Learn</a> • <a href="https://github.com/jina-ai/examples">Examples</a> • <a href="#contributing">Contribute</a> • <a href="https://jobs.jina.ai">Jobs</a> • <a href="http://jina.ai">Website</a> • <a href="http://slack.jina.ai">Slack</a>
</p>


## Installation

| 📦<br><sub><sup>x86/64,arm/v6,v7,[v8 (Apple M1)](https://github.com/jina-ai/jina/issues/1781)</sup></sub> | On Linux/macOS & Python 3.7/3.8/[3.9](https://github.com/jina-ai/jina/issues/1801) | Docker Users|
| --- | --- | --- |
| Standard | `pip install -U jina` | `docker run jinaai/jina:latest` |
| <sub>Daemon</sub> | <sub>`pip install -U "jina[daemon]"`</sub> | <sub>`docker run --network=host jinaai/jina:latest-daemon`</sub> |
| <sub>With Extras</sub> | <sub>`pip install -U "jina[devel]"`</sub> | <sub>`docker run jinaai/jina:latest-devel`</sub> |
| <sub>Dev/Pre-Release</sub> | <sub>`pip install --pre jina`</sub> | <sub>`docker run jinaai/jina:master`</sub> |

Version identifiers [are explained here](https://github.com/jina-ai/jina/blob/master/RELEASE.md). To install Jina with extra dependencies [please refer to the docs](https://docs.jina.ai/chapters/install/via-pip.html). Jina can run on [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). We welcome the community to help us with [native Windows support](https://github.com/jina-ai/jina/issues/1252).

## Jina "Hello, World!" 👋🌍

Just starting out? Try Jina's "Hello, World" - a simple image neural search demo for [Fashion-MNIST](https://hanxiao.io/2018/09/28/Fashion-MNIST-Year-In-Review/). No extra dependencies needed, simply run:

```bash
jina hello-world
```

...or even easier for Docker users, **no install required**:

```bash
docker run -v "$(pwd)/j:/j" jinaai/jina hello-world --workdir /j && open j/hello-world.html  
# replace "open" with "xdg-open" on Linux
```

<details>
<summary>Click here to see console output</summary>

<p align="center">
  <img src="https://github.com/jina-ai/jina/blob/master/.github/images/hello-world-demo.png?raw=true" alt="hello world console output">
</p>

</details>
This downloads the Fashion-MNIST training and test dataset and tells Jina to index 60,000 images from the training set. Then it randomly samples images from the test set as queries and asks Jina to retrieve relevant results. The whole process takes about 1 minute, and after running opens a webpage and shows results:

<p align="center">
  <img src="https://github.com/jina-ai/jina/blob/master/.github/images/hello-world.gif?raw=true" alt="Jina banner" width="80%">
</p>

Intrigued? Play with different options:

```bash
jina hello-world --help
```

## Get Started

|     |   |
| --- |---|
| 🥚  | [CRUD Functions](#crud-functions) |
| 🐣  | [Flow](#flow) • [Visualize](#visualize) • [Feed Data](#feed-data) • [Fetch Result](#fetch-result) • [Construct Document](#construct-document) • [Add Logic](#add-logic) • [Inter & Intra Parallelism](#inter--intra-parallelism) • [Decentralize](#decentralized-flow) • [Asynchronous](#asynchronous-flow) |
| 🐥 | [Customize Encoder](#customize-encoder) • [Test Encoder](#test-encoder-in-flow) • [Parallelism & Batching](#parallelism--batching) • [Add Data Indexer](#add-data-indexer) • [Compose Flow from YAML](#compose-flow-from-yaml) • [Search](#search) • [Evaluation](#evaluation) • [REST Interface](#rest-interface) |

#### CRUD Functions
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-crud-functions.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

First we look at basic CRUD operations. In Jina, CRUD corresponds to four functions: `index` (create), `search` (read), `update`, and `delete`. With Documents below as an example:
```python
import numpy as np
from jina import Document
docs = [Document(id='🐲', embedding=np.array([0, 0]), tags={'guardian': 'Azure Dragon', 'position': 'East'}),
        Document(id='🐦', embedding=np.array([1, 0]), tags={'guardian': 'Vermilion Bird', 'position': 'South'}),
        Document(id='🐢', embedding=np.array([0, 1]), tags={'guardian': 'Black Tortoise', 'position': 'North'}),
        Document(id='🐯', embedding=np.array([1, 1]), tags={'guardian': 'White Tiger', 'position': 'West'})]
```

Let's build a Flow with a simple indexer: 

```python
from jina import Flow
f = Flow().add(uses='_index')
```

`Document` and `Flow` are basic concepts in Jina, which will be explained later. `_index` is a built-in embedding + structured storage that one can use out of the box.

<table>
  <tr>
    <td>
    <b>Index</b>
    </td>
    <td>

```python
# save four docs (both embedding and structured info) into storage
with f:
    f.index(docs, on_done=print)
```

</tr>
  <tr>
    <td>
    <b>Search</b>
    </td>
    <td>

```python
# retrieve top-3 neighbours of 🐲, this print 🐲🐦🐢 with score 0, 1, 1 respectively 
with f:
    f.search(docs[0], top_k=3, on_done=lambda x: print(x.docs[0].matches))
```

<sup>

```json
{"id": "🐲", "tags": {"guardian": "Azure Dragon", "position": "East"}, "embedding": {"dense": {"buffer": "AAAAAAAAAAAAAAAAAAAAAA==", "shape": [2], "dtype": "<i8"}}, "score": {"opName": "NumpyIndexer", "refId": "🐲"}, "adjacency": 1}
{"id": "🐦", "tags": {"position": "South", "guardian": "Vermilion Bird"}, "embedding": {"dense": {"buffer": "AQAAAAAAAAAAAAAAAAAAAA==", "shape": [2], "dtype": "<i8"}}, "score": {"value": 1.0, "opName": "NumpyIndexer", "refId": "🐲"}, "adjacency": 1}
{"id": "🐢", "tags": {"guardian": "Black Tortoise", "position": "North"}, "embedding": {"dense": {"buffer": "AAAAAAAAAAABAAAAAAAAAA==", "shape": [2], "dtype": "<i8"}}, "score": {"value": 1.0, "opName": "NumpyIndexer", "refId": "🐲"}, "adjacency": 1}
```
</sup>

</tr>
  <tr>
    <td>
    <b>Update</b>
    </td>
    <td>

```python
# update 🐲 embedding in the storage
docs[0].embedding = np.array([1, 1])
with f:
    f.update(docs[0])
```

</tr>
  <tr>
    <td>
    <b>Delete</b>
    </td>
    <td>

```python
# remove 🐦🐲 Documents from the storage
with f:
    f.delete(['🐦', '🐲'])
```

</tr>
</table>

Get the vibe? Now we are talking! Let's learn more about the basic concepts and features in Jina.

#### Flow
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-create-flow.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

Jina provides a high-level [Flow API](https://101.jina.ai) to simplify building search/index workflows. To create a new Flow:

```python
from jina import Flow
f = Flow().add()
```

This creates a simple Flow with one [Pod](https://101.jina.ai). You can chain multiple `.add()`s in a single Flow.

#### Visualize
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-visualize-a-flow.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

To visualize the Flow, simply chain it with `.plot('my-flow.svg')`. If you are using a Jupyter notebook, the Flow object will be automatically displayed inline *without* `plot`:

<img src="https://github.com/jina-ai/jina/blob/master/.github/simple-flow0.svg?raw=true"/>

`Gateway` is the entrypoint of the Flow. 

#### Feed Data
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-feed-data.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

To use a Flow, open it via `with` context manager, like you would open a file in Python. Now let's create some empty document and index it:

```python
from jina import Document

with Flow().add() as f:
    f.index((Document() for _ in range(10)))
```

Flow supports CRUD operations: `index`, `search`, `update`, `delete`. Besides, it also provides sugary syntax on common data type such as files, text, and `ndarray`.

```python
with f:
    f.index_ndarray(numpy.random.random([4,2]), on_done=print)  # index ndarray data, document sliced on first dimension
    f.index_lines(['hello world!', 'goodbye world!'])  # index textual data, each element is a document
    f.index_files(['/tmp/*.mp4', '/tmp/*.pdf'])  # index files and wildcard globs, each file is a document
```

#### Fetch Result
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-fetch-result.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

Once a request is done, callback functions are fired. Jina Flow implements Promise-like interface, you can add callback functions `on_done`, `on_error`, `on_always` to hook different event. In the example below, our Flow passes the message then prints the result when success. If something wrong, it beeps. Finally, the result is written to `output.txt`.

```python
def beep(*args):
    # make a beep sound
    import os
    os.system('echo -n "\a";')


with Flow().add() as f, open('output.txt', 'w') as fp:
    f.index(numpy.random.random([4, 5, 2]),
            on_done=print, on_error=beep, on_always=lambda x: fp.write(x.json()))
```


#### Construct Document
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-construct-document.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

`Document` is [Jina's primitive data type](https://hanxiao.io/2020/11/22/Primitive-Data-Types-in-Neural-Search-System/#primitive-types). It can contain text, image, array, embedding, URI, and accompanied by rich meta information. It can be recurred both vertically and horizontally to have nested documents and matched documents. To construct a Document, one can use:

```python
import numpy
from jina import Document

doc1 = Document(content=text_from_file, mime_type='text/x-python')  # a text document contains python code
doc2 = Document(content=numpy.random.random([10, 10]))  # a ndarray document
doc1.chunks.append(doc2)  # doc2 is now a sub-document of doc1
```

<details>
  <summary>Click here to see more about MultimodalDocument</summary>
  

#### MultimodalDocument
  
A `MultimodalDocument` is a document composed of multiple `Document` from different modalities (e.g. text, image, audio).
 
Jina provides multiple ways to build a multimodal Document. For example, one can provide the modality names and the content in a `dict`:
  
```python
from jina import MultimodalDocument
document = MultimodalDocument(modality_content_map={
    'title': 'my holiday picture',
    'description': 'the family having fun on the beach',
    'image': PIL.Image.open('path/to/image.jpg')
})
```

One can also compose a `MultimodalDocument` from multiple `Document` directly:
  
```python
from jina.types import Document, MultimodalDocument

doc_title = Document(content='my holiday picture', modality='title')
doc_desc = Document(content='the family having fun on the beach', modality='description')
doc_img = Document(content=PIL.Image.open('path/to/image.jpg'), modality='description')
doc_img.tags['date'] = '10/08/2019' 

document = MultimodalDocument(chunks=[doc_title, doc_description, doc_img])
```

##### Fusion Embeddings from Different Modalities

To extract fusion embeddings from different modalities Jina provides `BaseMultiModalEncoder` abstract class, which has a unqiue `encode` interface.

```python
def encode(self, *data: 'numpy.ndarray', **kwargs) -> 'numpy.ndarray':
    ...
```

`MultimodalDriver` provides `data` to the `MultimodalDocument` in the correct expected order. In this example below, `image` embedding is passed to the endoder as the first argument, and `text` as the second.

```yaml
!MyMultimodalEncoder
with:
  positional_modality: ['image', 'text']
requests:
  on:
    [IndexRequest, SearchRequest]:
      - !MultiModalDriver {}
```

Interested readers can refer to [`jina-ai/example`: how to build a multimodal search engine for image retrieval using TIRG (Composing Text and Image for Image Retrieval)](https://github.com/jina-ai/examples/tree/master/multimodal-search-tirg) for the usage of `MultimodalDriver` and `BaseMultiModalEncoder` in practice.

</details>
  
#### Add Logic
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-add-logic.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

To add logic to the Flow, use the `uses` parameter to attach a Pod with an [Executor](https://101.jina.ai/#executors). `uses` accepts multiple value types including class name, Docker image, (inline) YAML or built-in shortcut.


```python
f = (Flow().add(uses='MyBertEncoder')  # class name of a Jina Executor
           .add(uses='docker://jinahub/pod.encoder.dummy_mwu_encoder:0.0.6-0.9.3')  # the image name
           .add(uses='myencoder.yml')  # YAML serialization of a Jina Executor
           .add(uses='!WaveletTransformer | {freq: 20}')  # inline YAML config
           .add(uses='_pass')  # built-in shortcut executor
           .add(uses={'__cls': 'MyBertEncoder', 'with': {'param': 1.23}}))  # dict config object with __cls keyword
```

The power of Jina lies in its decentralized architecture: each `add` creates a new Pod, and these Pods can be run as a local thread/process, a remote process, inside a Docker container, or even inside a remote Docker container.

#### Inter & Intra Parallelism
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-inter-intra-parallelism.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

Chaining `.add()`s creates a sequential Flow. For parallelism, use the `needs` parameter:

```python
f = (Flow().add(name='p1', needs='gateway')
           .add(name='p2', needs='gateway')
           .add(name='p3', needs='gateway')
           .needs(['p1','p2', 'p3'], name='r1').plot())
```

<img src="https://github.com/jina-ai/jina/blob/master/.github/simple-plot3.svg?raw=true"/>

`p1`, `p2`, `p3` now subscribe to `Gateway` and conduct their work in parallel. The last `.needs()` blocks all Pods until they finish their work. Note: parallelism can also be performed inside a Pod using `parallel`:

```python
f = (Flow().add(name='p1', needs='gateway')
           .add(name='p2', needs='gateway')
           .add(name='p3', parallel=3)
           .needs(['p1','p3'], name='r1').plot())
```

<img src="https://github.com/jina-ai/jina/blob/master/.github/simple-plot4.svg?raw=true"/>

#### Decentralized Flow
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=decentralized-flow.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

A Flow does not have to be local-only, one can put any Pod to remote(s). In the example below, with the `host` keyword `gpu-pod` is put to a remote machine for parallelization, whereas other pods stay local. Extra file dependencies that need to be uploaded are specified via the `upload_files` keyword. 

<table>
    <tr>
    <td>123.456.78.9</td>
    <td>

```bash
# have docker installed
docker run --name=jinad --network=host -v /var/run/docker.sock:/var/run/docker.sock jinaai/jina:latest-daemon --port-expose 8000
# to stop it
docker rm -f jinad
```

</td>
</tr>
  <tr>
    <td>
    Local
    </td>
    <td>

```python
import numpy as np
from jina import Flow

f = (Flow()
     .add()
     .add(name='gpu_pod',
          uses='mwu_encoder.yml',
          host='123.456.78.9:8000',
          parallel=2,
          upload_files=['mwu_encoder.py'])
     .add())

with f:
    f.index_ndarray(np.random.random([10, 100]), output=print)
```
</tr>

</table>

We provide a demo server on `cloud.jina.ai:8000`, give the following snippet a try!

```python
from jina import Flow

with Flow().add().add(host='cloud.jina.ai:8000') as f:
    f.index(['hello', 'world'])
```

#### Asynchronous Flow
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-inter-intra-parallelism.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

Synchronous from outside, Jina runs asynchronously underneath: it manages the eventloop(s) for scheduling the jobs. If user wants more control over the eventloop, then `AsyncFlow` comes to use. 

Unlike `Flow`, the CRUD of `AsyncFlow` accepts input & output functions as [async generator](https://www.python.org/dev/peps/pep-0525/). This is useful when your data sources involves other asynchronous libraries (e.g. motor for MongoDB):

```python
from jina import AsyncFlow

async def input_fn():
    for _ in range(10):
        yield Document()
        await asyncio.sleep(0.1)

with AsyncFlow().add() as f:
    async for resp in f.index(input_fn):
        print(resp)
```

`AsyncFlow` is particular useful when Jina is using as part of the integration, where another heavy-lifting job is running concurrently:

```python
async def run_async_flow_5s():  # WaitDriver pause 5s makes total roundtrip ~5s
    with AsyncFlow().add(uses='- !WaitDriver {}') as f:
        async for resp in f.index_ndarray(numpy.random.random([5, 4])):
            print(resp)

async def heavylifting():  # total roundtrip takes ~5s
    print('heavylifting other io-bound jobs, e.g. download, upload, file io')
    await asyncio.sleep(5)
    print('heavylifting done after 5s')

async def concurrent_main():  # about 5s; but some dispatch cost, can't be just 5s, usually at <7s
    await asyncio.gather(run_async_flow_5s(), heavylifting())

if __name__ == '__main__':
    asyncio.run(concurrent_main())
```

`AsyncFlow` is very useful when using Jina inside the Jupyter Notebook. As Jupyter/ipython already manages an eventloop and thanks to [`autoawait`](https://ipython.readthedocs.io/en/stable/interactive/autoawait.html), `AsyncFlow` can run out-of-the-box in Jupyter.

That's all you need to know for understanding the magic behind `hello-world`. Now let's dive into it!

### Breakdown of `hello-world`

|     |   |
| --- |---|
| 🥚  | [CRUD Functions](#crud-functions) |
| 🐣  | [Flow](#flow) • [Visualize](#visualize) • [Feed Data](#feed-data) • [Fetch Result](#fetch-result) • [Construct Document](#construct-document) • [Add Logic](#add-logic) • [Inter & Intra Parallelism](#inter--intra-parallelism) • [Decentralize](#decentralized-flow) • [Asynchronous](#asynchronous-flow) |
| 🐥 | [Customize Encoder](#customize-encoder) • [Test Encoder](#test-encoder-in-flow) • [Parallelism & Batching](#parallelism--batching) • [Add Data Indexer](#add-data-indexer) • [Compose Flow from YAML](#compose-flow-from-yaml) • [Search](#search) • [Evaluation](#evaluation) • [REST Interface](#rest-interface) |


#### Customize Encoder

Let's first build a naive image encoder that embeds images into vectors using an orthogonal projection. To do this, we simply inherit from `BaseImageEncoder`: a base class from the `jina.executors.encoders` module. We then override its `__init__()` and `encode()` methods.


```python
import numpy as np
from jina.executors.encoders import BaseImageEncoder

class MyEncoder(BaseImageEncoder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        np.random.seed(1337)
        H = np.random.rand(784, 64)
        u, s, vh = np.linalg.svd(H, full_matrices=False)
        self.oth_mat = u @ vh

    def encode(self, data: 'np.ndarray', *args, **kwargs):
        return (data.reshape([-1, 784]) / 255) @ self.oth_mat
```

Jina provides [a family of `Executor` classes](https://github.com/jina-ai/jina/tree/master/docs/chapters/101#the-executor-family), which summarize frequently-used algorithmic components in neural search. This family consists of encoders, indexers, crafters, evaluators, and classifiers, each with a well-designed interface. You can find the list of [all 107 built-in executors here](https://docs.jina.ai/chapters/all_exec.html). If they don't meet your needs, inheriting from one of them is the easiest way to bootstrap your own Executor. Simply use our Jina Hub CLI:


```bash
pip install jina[hub] && jina hub new
```

#### Test Encoder in Flow

Let's test our encoder in the Flow with some synthetic data:


```python
def validate(req):
    assert len(req.docs) == 100
    assert NdArray(req.docs[0].embedding).value.shape == (64,)

f = Flow().add(uses='MyEncoder')

with f:
    f.index_ndarray(numpy.random.random([100, 28, 28]), on_done=validate)
```


All good! Now our `validate` function confirms that all one hundred 28x28 synthetic images have been embedded into 100x64 vectors. 

#### Parallelism & Batching

By setting a larger input, you can play with `batch_size` and `parallel`:


```python
f = Flow().add(uses='MyEncoder', parallel=10)

with f:
    f.index_ndarray(numpy.random.random([60000, 28, 28]), batch_size=1024)
```

#### Add Data Indexer

Now we need to add an indexer to store all the embeddings and the image for later retrieval. Jina provides a simple `numpy`-powered vector indexer `NumpyIndexer`, and a key-value indexer `BinaryPbIndexer`. We can combine them in a single YAML file:

```yaml
!CompoundIndexer
components:
  - !NumpyInde