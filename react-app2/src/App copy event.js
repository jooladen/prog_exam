import './App.css';





function Article(p){
  return (
    <article>
      <h2>{p.title}</h2>{p.body}
    </article>
  );
}
// function Header(props){
//   console.log("props >>> ", props);
  
//   return( 
//     <header>
//       <h1><a href="/" onClick={function(event){
//         event.preventDefault();
//         props.onChangeMode();
//       }}>{props.title}</a></h1>
//     </header>
//   );
// }

// function Header(props){
//   console.log("props >>> ", props);
  
//   return( 
//     <header>
//       <h1><a href="/" onClick={event=>{
//         event.preventDefault();
//         props.onChangeMode();
//       }}>{props.title}</a></h1>
//     </header>
//   );
// }

function Header(props){
  console.log("props >>> ", props);
  
  return( 
    <header>
      <h1><a href="/" onClick={(event)=>{
        event.preventDefault();
        props.onChangeMode();
      }}>{props.title}</a></h1>
    </header>
  );
}

function Nav(props){
  const list = []

  for(let i = 0; i < props.data.length; i++){
    let t = props.data[i]
    list.push(<li key={t.id}>
        <a id={t.id} href={"/read/" + t.id} onClick={event=>{
          event.preventDefault();
          props.onChangeMode(event.target.id);
        }}>
          {t.title}
        </a>
      </li>) 
  }

  return (
    <nav>
      <ol>
        {list}
      </ol>
    </nav>
  );
}

function App() {
  const topics = [
    {"id" : 1,  "title" : 'html', "body" : 'html is ...'},
    {"id" : 2,  "title" : 'css', "body" : 'html is ...'},
    {"id" : 3,  "title" : 'javascript', "body" : 'javascript is ...'},
  ]

  return (
    <div>
      <Header title="REACT" onChangeMode={()=>{
        alert('Header');
      }}></Header>
      <Nav data={topics} onChangeMode={id=>{
        alert(id);
      }}></Nav> {/* 문자열은 위처럼, 배열객체를 던질때는 {} */}
      <Article title="Welcome" body='hello, WEB'></Article>
    </div>
  );

  // return (
  //   <div>
  //     <Header title="REACT" onChangeMode={function(){
  //       alert('Header');
  //     }}></Header>
  //     <Nav data={topics}></Nav> {/* 문자열은 위처럼, 배열객체를 던질때는 {} */}
  //     <Article title="Welcome" body='hello, WEB'></Article>
  //   </div>
  // );
}

export default App;
