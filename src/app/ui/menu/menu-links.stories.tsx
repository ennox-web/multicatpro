import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';

import MenuLinks from './menu-links';


const meta = {
    title: 'Menu/MenuLinks',
    component: MenuLinks,
    parameters: {
        layout: 'centered',
    },
    tags: ['autodocs'],
    decorators: [
        (Story) => (
            <div style={{ height: '100px', display: 'flex', alignItems: 'center' }}>
                <Story />
            </div>
        )
    ]
} satisfies Meta<typeof MenuLinks>;

export default meta;
type Story = StoryObj<typeof meta>;


export const Primary: Story = {

};
