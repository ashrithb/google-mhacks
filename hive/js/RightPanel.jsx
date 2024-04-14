import React, { useState } from 'react';
import Calendar from 'react-calendar';

export default function RightPanel() {
  const [value, onChange] = useState(new Date());

  return (
    <div className="panel">
      <iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=America%2FDetroit&bgcolor=%23ffffff&src=b2pidWNrZXRzOUBnbWFpbC5jb20&src=YWRkcmVzc2Jvb2sjY29udGFjdHNAZ3JvdXAudi5jYWxlbmRhci5nb29nbGUuY29t&src=ZW4udXNhI2hvbGlkYXlAZ3JvdXAudi5jYWxlbmRhci5nb29nbGUuY29t&color=%23039BE5&color=%2333B679&color=%230B8043" style={{border: 'solid 1px #777'}}  width="100%" height="600" ></iframe>
    </div>
  );
}

// export default RightPanel;