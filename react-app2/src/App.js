import './App.css';

function Header(props){
  //console.log("title >>> ", title);
  console.log("props >>> ", props);
  
  return( 
    <header>
      <h1><a href="/">{props.title}</a></h1>
    </header>
  );
}

function Nav(props){
  // const list = [
  //   <li><a href="/read/1">html</a></li>,
  //   <li><a href="/read/2">css</a></li>,
  //   <li><a href="/read/3">js</a></li>,
  // ]

  // console.log(props.data[0].title);
  // console.log(props.data[1].title);
  // console.log(props.data[2].title);
  
  const list = []

  for(let i = 0; i < props.data.length; i++){
    //list.push(<li>{props.data[i].title}</li>)
    let t = props.data[i]
    //console.log("t >>> ", t);
    //list.push(<li>{t.title}</li>)
    list.push(<li key={t.id}><a href={"/read/" + t.id}>{t.title}</a></li>)
    
    //console.log(list);
    
  }

  return (
    <nav>
      <ol>
        {list}
      </ol>
    </nav>
  );
}

function Article(p){
  return (
    <article>
      <h2>{p.title}</h2>{p.body}
    </article>
  );
}

function App() {
  // const topics = [
  //   {id : 1,  title : 'html', body : 'html is ...'},
  //   {id : 2,  title : 'css', body : 'html is ...'},
  //   {id : 3,  title : 'javascript', body : 'javascript is ...'},
  // ]

  //자바크립트의 객체는 키에 ""를 사용안해도 되지만
  //파이썬 딕셔너리는 키에 반드시 ""를 사용해야 한다.
  //그래서 항상 키에는 "" or ''를 붙이면 헷갈리지 않는다.
  const topics = [
    {"id" : 1,  "title" : 'html', "body" : 'html is ...'},
    {"id" : 2,  "title" : 'css', "body" : 'html is ...'},
    {"id" : 3,  "title" : 'javascript', "body" : 'javascript is ...'},
  ]

  return (
    <div>
      <Header title="REACT"></Header>
      <Nav data={topics}></Nav> {/* 문자열은 위처럼, 배열객체를 던질때는 {} */}
      <Article title="Welcome" body='hello, WEB'></Article>
    </div>
  );
}

export default App;
