import React, { useState } from 'react';
import Calendar from 'react-calendar';

export default function RightPanel() {
  const [value, onChange] = useState(new Date());

  return (
    <div className="panel">
      <iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=America%2FNew_York&bgcolor=%23ffffff&src=YWRpdGtrMjlAZ21haWwuY29t&src=YWRkcmVzc2Jvb2sjY29udGFjdHNAZ3JvdXAudi5jYWxlbmRhci5nb29nbGUuY29t&src=dW1pY2guZWR1X3JqNGU2dXRnc2ZodDBtazhzNGlqcTRyZHU4QGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20&src=ZW4udXNhI2hvbGlkYXlAZ3JvdXAudi5jYWxlbmRhci5nb29nbGUuY29t&src=Y190aGgwcGFlYW5yZGdsbmU3ZXI5N20zYWc5Z0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t&src=Y185ZjY2YWVlMmI3ZjQ2YjEyMzc3OTc2ZWQzZTlhZDQ4YzAyZGZkMjQ3YjcxZjU3ZmNkNGMwYmUwMWY3OGIxYmExQGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20&src=Y180MTIzZjAwYjBmMThhM2MwMmM3YjVkNWQwNTQ0NjEzMDgzNGFjMjBhYmU2OTY2MjE1ZjE2ZThlZmI2MWQ2NzQ1QGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20&color=%237986CB&color=%2333B679&color=%23F4511E&color=%230B8043&color=%23F4511E&color=%239E69AF&color=%23D81B60" style={{border: 'solid 1px #777'}} width="800" height="600" ></iframe>
    </div>
  );
}

// export default RightPanel;